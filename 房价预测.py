from sklearn import datasets, linear_model,svm
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd
import statsmodels.api as sm
path='D:/Desktop/housing.csv'
##多元线性回归：
class forcast:
    def __init__(self,filename=path):
        self.filename=filename
        data=pd.read_csv(self.filename)
        x=[]
        y=[]
        x_std=[]
        y_std=[]
        rm=[]
        ls=[]
        pt=[]
        me=[]
        for a,b,c,d in zip(data['RM'],data['LSTAT'],data['PTRATIO'],data['MEDV']):
            x.append([a,b,c])
            y.append(d)
            rm.append(a)
            ls.append(b)
            pt.append(c)
            me.append(d)
        (rm_min,rm_max,ls_min,ls_max,pt_min,pt_max,self.me_min,self.me_max)=(np.min(rm),np.max(rm),np.min(ls),np.max(ls),np.min(pt),np.max(pt),np.min(me),np.max(me))
        size=len(y)
        x=np.array(x)
        y=np.array(y)  
        for temp in x:
            x_std.append([(temp[0]-rm_min)/(rm_max-rm_min),(temp[1]-ls_min)/(ls_max-ls_min),(temp[2]-pt_min)/(pt_max-pt_min)])
        for temp in y:
            y_std.append((temp-self.me_min)/(self.me_max-self.me_min))
        x_std=np.array(x_std)
        y_std=np.array(y_std)
        idx_train=np.random.choice(np.arange(size),size=int(size*0.8),replace=False)
        self.x_train=x[idx_train]
        self.y_train=y[idx_train]
        self.x_train_std=x_std[idx_train]
        self.y_train_std=y_std[idx_train]
        idx_test=list(set(np.arange(size))-set(idx_train))
        self.x_test=x[idx_test]
        self.y_test=y[idx_test]
        self.x_test_std=x_std[idx_test]
        self.y_test_std=y_std[idx_test]

        
    def OLS_train(self):
        model=sm.OLS(self.y_train,self.x_train)
        result=model.fit()
        params=result.params
        return np.sum(self.x_test*params,1)
    
    def OLS_train_std(self):
        model=sm.OLS(self.y_train_std,self.x_train_std)
        result=model.fit()
        params=result.params
        y_pred_std=np.sum(self.x_test_std*params,1)
        y_pred=[]
        for temp in y_pred_std:
            y_pred.append(temp*(self.me_max-self.me_min)+self.me_min)         
        return y_pred
    
    def knn_regression(self,k):
        knn=KNeighborsRegressor(n_neighbors=k)
        knn.fit(self.x_train,self.y_train)
        return knn.predict(self.x_test)
    
    def knn_regression_std(self,k):
        knn=KNeighborsRegressor(n_neighbors=k)
        knn.fit(self.x_train_std,self.y_train_std)
        y_pred_std= knn.predict(self.x_test_std)
        y_pred=[]
        for temp in y_pred_std:
            y_pred.append(temp*(self.me_max-self.me_min)+self.me_min)         
        return y_pred
    
    def svm(self):
        clf=svm.SVC()
        clf.fit(self.x_train,self.y_train)
        return clf.predict(self.x_test)
    
    def svm_std(self):
        clf=svm.SVC()
        clf.fit(self.x_train_std,self.y_train_std)
        y_pred_std=clf.predict(self.x_test_std)
        y_pred=[]
        for temp in y_pred_std:
            y_pred.append(temp*(self.me_max-self.me_min)+self.me_min)         
        return y_pred
    
    def Random_forest(self):
        forest=RandomForestRegressor(n_estimators=1000,criterion='mse',random_state=1,n_jobs=-1)
        forest.fit(self.x_train, self.y_train)
        return forest.predict(self.x_test)
    
    def Random_forest_std(self):
        forest=RandomForestRegressor(n_estimators=1000,criterion='mse',random_state=1,n_jobs=-1)
        forest.fit(self.x_train_std, self.y_train_std)
        y_pred_std=forest.predict(self.x_test_std)
        y_pred=[]
        for temp in y_pred_std:
            y_pred.append(temp*(self.me_max-self.me_min)+self.me_min)         
        return y_pred

    def test(self,pred):
        temp=self.y_test-pred
        print('MSE = ',np.sum(temp**2))
        print('Error mean percent(MAPE) is ',np.sum(np.abs(temp/self.y_test))/len(self.y_test)*100,'%')
        
    
model=forcast()
print('OLS results:')
model.test(model.OLS_train())
print('The std results:')
model.test(model.OLS_train_std())
print('\nKnn results:')
model.test(model.knn_regression(6))  ##参数可行性分析说明
print('The std results:')
model.test(model.knn_regression_std(6))
print('\nSVM results:')
model.test(model.svm())
print('\nRandom Forest results:')
model.test(model.Random_forest())
print('The std results:')
model.test(model.Random_forest_std())