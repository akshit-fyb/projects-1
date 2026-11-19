from pathlib import Path
import json, joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'synthetic_travel_expenses.csv'
MODEL_DIR=ROOT/'ml'/'models'; MODEL_DIR.mkdir(exist_ok=True)

def main():
    df=pd.read_csv(DATA)
    X=df.drop(columns=['total_cost']); y=df['total_cost']
    cat=X.select_dtypes(include='object').columns.tolist(); num=[c for c in X.columns if c not in cat]
    prep=ColumnTransformer([('cat',OneHotEncoder(handle_unknown='ignore'),cat),('num',StandardScaler(),num)])
    models={
      'Linear Regression':LinearRegression(),
      'Decision Tree':DecisionTreeRegressor(max_depth=10,random_state=42),
      'Random Forest':RandomForestRegressor(n_estimators=180,max_depth=14,random_state=42,n_jobs=-1),
      'Gradient Boosting':GradientBoostingRegressor(random_state=42)
    }
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,random_state=42)
    results={}; fitted={}
    for name,model in models.items():
        pipe=Pipeline([('preprocess',prep),('model',model)]); pipe.fit(Xtr,ytr); pred=pipe.predict(Xte)
        mse=mean_squared_error(yte,pred)
        results[name]={'MAE':float(mean_absolute_error(yte,pred)),'MSE':float(mse),'RMSE':float(mse**0.5),'R2':float(r2_score(yte,pred))}
        fitted[name]=pipe
    best=min(results,key=lambda k:results[k]['RMSE'])
    joblib.dump(fitted[best],MODEL_DIR/'travel_cost_model.joblib')
    (MODEL_DIR/'metrics.json').write_text(json.dumps({'dataset':'synthetic supplementary dataset','rows':len(df),'best_model':best,'results':results},indent=2))
    print(json.dumps({'best_model':best,'results':results},indent=2))

if __name__=='__main__': main()
