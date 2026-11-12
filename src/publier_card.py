
from pathlib import Path

import mlflow
from mlflow import MlflowClient


# 1. Connexion au serveur MLflow
mlflow.set_tracking_uri('http://127.0.0.1:5000')


# 2. Creer le client MLflow
c = MlflowClient()


# 3. Recuperer la version de production
v = c.get_model_version_by_alias(
    'fraude',
    'production'
)


# 4. Recuperer le run des explications
run_id = Path(
    'reports/run_xai.txt'
).read_text().strip()


# 5. Attacher la Model Card au run XAI
with mlflow.start_run(run_id=run_id):
    mlflow.log_artifact('MODEL_CARD.md')


# 6. Lire le contenu de la Model Card
card = Path(
    'MODEL_CARD.md'
).read_text(encoding='utf-8')


# 7. Ajouter la Model Card comme description
# de la version du modele
c.update_model_version(
    'fraude',
    v.version,
    description=card
)


# 8. Ajouter un tag au modele
c.set_model_version_tag(
    'fraude',
    v.version,
    'model_card',
    'MODEL_CARD.md, run ' + run_id[:8]
)


# 9. Confirmation
print(
    'Model Card attachee a fraude v'
    + v.version,
    'et au run',
    run_id[:8]
)
