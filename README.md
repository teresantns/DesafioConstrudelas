<div id="top"></div>

# Desafio Final Construdelas

This is the final individual project of [Gama Academy](https://www.gama.academy/)'s  Construdelas Python training in partnership with [Juntos Somos +](https://www.juntossomosmais.com.br/), created by participant [Teresa Seabra Antunes](https://github.com/teresantns).

The goal of this project was to develop an API and create endpoints related to a `Loyalty Program` system. We were challenged to create four basic endpoints functionalities: for creating a referral; accepting a referral; getting information on a specific referral; and getting information on all registered referrals. 

The API was developed with [Django](https://www.djangoproject.com/) and [Django REST framework](https://www.django-rest-framework.org/)

## Table of Contents

<details>
<summary>Click to expand!</summary>
  
- [Running the project](#run)
  - [API endpoints](#endpoints)
- [How the project was carried out](#carry)
  - [Planning](#plan)
  - [Git branching](#git)
  - [Documentation](#doc)
  - [Testing](#test)
  - [Logging](#log)
  - [Docker](#docker)
- [Some considerations](#considerations)
  - [A 'bug' to take into consideration](#bug)
  - [What's next?](#next)
  
</details>


# 🚀&nbsp; Running the project <a name="run"></a>
This project uses [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/). First, clone the repository to create a local copy of the directories:

```shell
git clone https://github.com/teresantns/DesafioConstrudelas
```

### Running the API <a name="run1"></a>
Run `docker-compose up --build app` (wait for the docker container to build) and the API will be available on port 8000 (http://localhost:8000) 

### Running the tests <a name="run2"></a>
Simply run `docker-compose up --build tests` to run the tests, and they will run on terminal!
<p align="right">(<a href="#top">back to top</a>)</p>

## 📌 API endpoints: <a name="endpoints"></a>
- **POST** - `/user/` - Creates a new user.
- **GET** - `/user/<str:cpf>/` - Gets information of the user with the CPF specified on the url.
- **PUT** - `/user/<str:cpf>/` - Updates information of the user with the CPF specified on the url.
- **GET** - `/all-referrals/` - 
Gets the data of all referrals on database.
- **GET** - `/all-referrals/<str:cpf>/` - Gets the data of all referrals on database made by specific user, whose CPF is passed on the URL path.
- **GET** - `/referral/<str:cpf>/` -Gets the data of a specific referral on database given the CPF of the referred person, which is passed on the URL path.
- **POST** - `/create-referral/` - Creates a Referral, following the rules set by the challenge.
- **GET** - `/accept-referral/<str:cpf>/` - Gets a specific referral, allowing its acceptance. The referred person's CPF is passed on the URL path.
- **PUT** - `/accept-referral/<str:cpf>/` - Updates referral, allowing its acceptance ('true' on status field). The CPF of referred person is passed on the URL path.

For a more detailed documentation of each route, with examples of requests and returns, check out the [Postman documentation](https://documenter.getpostman.com/view/18867856/UVREij7v), and to see an example of how the project works, check out this video (COLOCAR LINK DO VIDEO)

<p align="right">(<a href="#top">back to top</a>)</p>

# How the project was carried out <a name="carry"></a>

## 📆 Planning <a name="plan"></a>
<p align="right">(<a href="#top">back to top</a>)</p>

## 🌿 Git branching <a name="git"></a>

<p align="right">(<a href="#top">back to top</a>)</p>

## ℹ️ Documentation <a name="doc"></a>

<p align="right">(<a href="#top">back to top</a>)</p>

## ✔️ Testing <a name="test"></a>

<p align="right">(<a href="#top">back to top</a>)</p>


## 🔎 Logging <a name="log"></a>

<p align="right">(<a href="#top">back to top</a>)</p>

## 📦 Docker <a name="docker"></a>
<p align="right">(<a href="#top">back to top</a>)</p>

# Some considerations <a name="considerations"></a>

## 🐛 A 'bug' to take into consideration <a name="bug"></a>
<p align="right">(<a href="#top">back to top</a>)</p>

## ➡️ What's next? <a name="next"></a>
<p align="right">(<a href="#top">back to top</a>)</p>
