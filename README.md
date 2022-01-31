
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/GPL-3.0)


# Mahao Backend

This is the backend serving the APIs for Mahao, which is a house 
recommendation Android application. House owners/agents will be able to 
post their houses and prospective tenants to find houses.


## Tech Stack

**Client:** Vue

**Server:** Python, FastAPI, Docker, Docker Compose, PostgreSQL, Go, Gorse, MySQL


## Documentation

The backend is build using Python and FastAPI. The application interfaces 
with an instance of the Gorse Recommendation engine to generate property 
reommendations. View the [FastAPI backend documentation](./backend/README.md)
and the [Gorse backend documentation](https://github.com/zhenghaoz/gorse/blob/master/README.md).
## Environment Variables

To run this project, you will need to add the following [environment variables](./.env.example) 
to your .env file

## Demo

![](./screenshots/mahao_backend.gif)

## Deployment

After cloning/forking the project and updating the environment variables, 
start the servers by running the following on the root folder:
```bash
  sudo docker-compose up -d
```
    
## Related

Here are some related projects:

[Full Stack FastAPI and PostgreSQL - Base Project Generator](https://github.com/tiangolo/full-stack-fastapi-postgresql)

[gorse: Go Recommender System Engine](https://github.com/zhenghaoz/gorse)


## Authors

- [@tonyawino](https://www.github.com/tonyawino)


## License

[GPL v3](https://opensource.org/licenses/GPL-3.0)

    The Mahao Backend serves APIs for the Mahao Android app.
    Copyright (C) 2022  Tony Awino

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

