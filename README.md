# Task Manager 

Task Manager to prosta aplikacja stworzona w Django i osadzona na Dockerze której celem jest zarządzanie zadaniami

## Wymagania

- Docker >= 27
- Docker Compose >= 2.29

## Instalacja 

### 1. Sklonuj repozytorium:

    git clone https://github.com/Cukierrrrr/taskmanager.git

### 2. Zbuduj i uruchom komponenty

Zbuduj komponenty Dockera, na których działa aplikacja
    
    docker-compose up --build -d

### 3. Utwórz i wprowadź migracje

Wykonaj poniższe polecenie aby utworzyć migracje

    docker-compose exec web python manage.py makemigrations

Aby wprowadzić migracje dla bazy danych wykonaj polecenie

    docker-compose exec web python manage.py migrate

## Użycie

### 1. Uruchom kontenery(Jesli jeszcze nie zostało to zrobione)

Jeśli jeszcze nie uruchmiłeś kontenerów wywołaj polecenie

    docker-compose up -d

### 2. Utwórz administratora

Aby mieć dostęp do aplikacji stwórz administratora poleceniem

    docker-compose exec web python manage.py createsuperuser

### 3. Wejdź do aplikacji

Kiedy kontenery już się odpalą aplikacja będzie dostępna pod adresem

http://localhost:8000

### 4. Zatrzymaj aplikację

Aby zatrzymać aplikację wywołaj polecenie

    docker-compose down

## Testowanie

### 1. Uruchom kontenery(Jęsli jeszcze nie zostało to zrobione)

Jeśli jeszcze nie uruchmiłeś kontenerów wywołaj polecenie

    docker-compose up -d

### 2. Uruchom testy

Aby uruchomić testy wywołaj polecenie

    docker-compose exec web pytest

## Contributing 

Znalazłeś błąd? Zgłoś issue lub wyślij pull request. 

## Licencja 

MIT © 2025 Rafał Filipczak