from classes.Gene import *
from classes.Data import *
from classes.Model import *
import random
import gc
import numpy as np
import copy
from datetime import timedelta
import datetime
import datetime as dt


class Individual(object):    
    def __init__(self, params, full_initiate=False):
        self.params = params
        self.genes = []
        self.training_data = []
        self.test_data = []
        self.model = []
        self.fitness = []
        self.data_set_num = -1
        
        self.initGenes()
        
        if full_initiate:
            self.initModel()
            self.calculateFitness()
            del(self.training_data)
            self.training_data = []
            self.test_data = []
            gc.collect()
        
    def initGenes(self):
        
        model_to_use = self.params['machineModelType']
        
        
        # COMMON FEATURES
        self.genes.append(Gene('i_RSI_timeperiod_short',[4,7,10]))
        self.genes.append(Gene('i_RSI_timeperiod_medium',[5,7,10,14]))
        self.genes.append(Gene('i_MA_timeperiod_short',[6,8,10,15]))
        self.genes.append(Gene('i_MA_timeperiod_medium_1',[10,15,30]))
        self.genes.append(Gene('i_MA_timeperiod_medium_2',[75,100,150,175,200]))
        self.genes.append(Gene('i_MA_timeperiod_long',[75,100,200,300]))
        self.genes.append(Gene('i_BB_timeperiod',[3,5,10,15]))
        self.genes.append(Gene('i_ATR_timeperiod',[14,21,28,32,35]))
        self.genes.append(Gene('i_LL_timeperiod',[3,5,7,9,11]))
        self.genes.append(Gene('i_HH_timeperiod',[5,7,10,15]))
        self.genes.append(Gene('i_LC_timeperiod',[7,9,11,13]))
        self.genes.append(Gene('i_HC_timeperiod',[15,20,30,40]))
        self.genes.append(Gene('i_previous_periods',[3,5,7,9,11]))
        self.genes.append(Gene('i_STOCH_fastk',[2,3,5,7,8,9]))
        self.genes.append(Gene('i_STOCH_fastd',[2,3,5,7,9]))        
        
        
        if model_to_use == 'SVM':
            a = 2 # Inget speciellt ännu
        
        if model_to_use == 'XGB':       
            self.genes.append(Gene('f_Model_XGB_learning_rate',[0.00001,0.0001, 0.001]))
            self.genes.append(Gene('f_Model_XGB_gamma',[0.001,0.01,0.1,0.2,0.3,1]))
            self.genes.append(Gene('i_Model_XGB_max_depth',[7,9,11,13]))
            self.genes.append(Gene('f_Model_XGB_colsample_bytree',[0.5,0.7,0.8]))
            self.genes.append(Gene('f_Model_XGB_subsample',[0.2,0.3,0.4,0.5,0.7,0.8]))
            self.genes.append(Gene('i_Model_XGB_min_child_weight',[1,3,5,7,9]))
            self.genes.append(Gene('i_Model_XGB_n_estimators',[250,400,750,500,600]))        
        
        if model_to_use == 'NB':  # Naive Bayes
            a = 2 #
        
        if model_to_use == 'LDA':
            a = 2 #
        
        if model_to_use == 'KNN':
            self.genes.append(Gene('i_num_neighbors',[2,3,4,5]))    
        
        #self.genes.append(Gene('',[]))
        
    
    def gene_dict(self):
        gdict = {}
        for g in self.genes:
            gdict[g.name] = g.value
        return gdict
    
    def initModel(self):
        self.model = Model(self)
    
    def findTrainTestDates(self):
        start_of_year = datetime.date(2019,1,1)
        all_days = list(range(0,300))
        
        num_train_days = 50
        earliest_test_date = start_of_year + timedelta(days=55)
        
        for i in range(100):
            day_of_year = random.choice(all_days)
            #print('Day of year: {}'.format(day_of_year))
            test_date_start = (start_of_year + timedelta(days = day_of_year))
            test_date_end = test_date_start + timedelta(days=1)
            if test_date_start.weekday() in range(4,7) or test_date_start < earliest_test_date:
                continue
            train_date_start = test_date_start - timedelta(days=50)
            train_date_end = test_date_start - timedelta(days=1)
            print('Train start: {} end: {}'.format(train_date_start.strftime("%y-%m-%d"),train_date_end.strftime("%y-%m-%d")))
            print('Test start: {} end: {}'.format(test_date_start.strftime("%y-%m-%d"),test_date_end.strftime("%y-%m-%d")))
            break
        
        return train_date_start, train_date_end, test_date_start, test_date_end

    def getFilteredDF(self, df, start_date, end_date):
        df['date'] = pd.to_datetime(df['Datetime']).dt.date
        mask = (df['date']>=start_date) & (df['date']<=end_date)
        df = df.loc[mask]
        df = df.drop('date', axis=1)
        return df
    
        
    def calculateFitness(self):
        fitness_local=[]
        
        print('-------------------')
        print('Fitness calculation')
        print('')   
        
        for num_train in range(10):
            print('-------------------')
            print('Training number: {}'.format(num_train+1))
            data_obj = Data(self)
            
            train_date_start, train_date_end, test_date_start, test_date_end = self.findTrainTestDates()
            
            train_df = self.getFilteredDF(data_obj.df, train_date_start, train_date_end)
            test_df = self.getFilteredDF(data_obj.df, test_date_start, test_date_end)
            
            X_train, y_train = data_obj.getXy(train_df)
            X_train = self.model.scaleFitTransform(X_train)
            print('Training on {} samples'.format(X_train.shape[0]))

            X_test, y_test = data_obj.getXy(test_df, balance=False)
            X_test = self.model.scaleTransform(X_test)
            print('Testing on {} samples'.format(X_test.shape[0]))

            self.model.train(X_train, y_train)
            fitness_local.append(self.model.evaluate(X_test, y_test))       
        
        _min = np.min(fitness_local)
        _min = np.float('{:0.1f}'.format(_min))
        self.min =_min
        
        _max = np.max(fitness_local)
        _max = np.float('{:0.1f}'.format(_max))
        self.max = _max
        
        _avg = np.average(fitness_local)
        _avg = np.float('{:0.1f}'.format(_avg))
        self.avg = _avg        
        
        print('Min: {}, Max: {}, Avg: {}'.format(self.min, self.max, self.avg))
        
        self.fitness = _avg
        
        self.printFitness()
        
        self.dumpParameters()
        
        del(self.training_data)
        self.training_data = []
        self.test_data = []
        del(self.model)
        self.model = []
        gc.collect()

        
    def printFitness(self):
        print('Fitness: {}%'.format(self.fitness))
    
    def printGenes(self):
        for g in self.genes:
            print('{}: {}'.format(g.name,g.value))
                     
    def printGeneType(self):
        for g in self.genes:
            print('{}: {}'.format(g.name,type(g.value)))        
            
    def dumpParameters(self):
        simulations_log_file = 'simulation_log_' + self.params['machineModelType'] + '.csv'
        print('Writing to log file: {}'.format(simulations_log_file))
        try:
            df_parameters = pd.read_csv(simulations_log_file)
        except:
            df_parameters = pd.DataFrame(columns=self.getColumnNames())

        df_parameters = df_parameters.append(pd.DataFrame(columns=df_parameters.columns,data=[self.getValues()]))

        df_parameters.to_csv(simulations_log_file,index=False)       

            
    def getColumnNames(self):
        out = []
        for g in self.genes:
            name = g.name
            out.append(name[2:])
        out.append('Fitness')
        out.append('Min')
        out.append('Max')
        out.append('Avg')
        return out
    
    def getValues(self):
        out = []
        for g in self.genes:
            out.append(g.value)
        out.append(self.fitness)
        out.append(self.min)
        out.append(self.max)
        out.append(self.avg)
        return out        
            
            
            
            
            
            
            
            
            
            
            
            