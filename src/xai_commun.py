
import mlflow
import mlflow.sklearn
import pandas as pd

from mlflow import MlflowClient
from sklearn.model_selection import train_test_split

# Connexion au serveur MLflow
mlflow.set_tracking_uri('http://127.0.0.1:5000')

# Modele et alias de production
NOM, ALIAS = 'fraude', 'production'

# Recuperer la version du modele
VERSION = MlflowClient().get_model_version_by_alias(NOM, ALIAS)

# Charger le modele entraine
m = mlflow.sklearn.load_model(f'models:/{NOM}@{ALIAS}')

# Charger les donnees du TP02
df = pd.read_csv('data/transactions.csv')

# Separer les variables et la cible
X, y = df.drop(columns='fraude'), df['fraude']

# Reproduire le decoupage du TP02
Xtr, Xte, ytr, yte = train_test_split(
    X, y,
    test_size=0.25,
    random_state=42
)

# Transaction de Mme Benali
CAS = pd.DataFrame([{
    'montant': 1800.0,
    'anciennete': 30,
    'freq_24h': 4,
    'nuit': 1
}])
