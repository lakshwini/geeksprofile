#!/bin/bash
echo "🚀 Déploiement en production..."

cd /home/ubuntu/geeksprofile

# Pull la dernière image depuis Docker Hub
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d

# Vérification
echo "📊 Statut des containers :"
docker-compose -f docker-compose.prod.yml ps

echo "✅ Déploiement terminé !"
echo "🌐 Application accessible sur: http://localhost:5000"