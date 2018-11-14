# cgmatch
Add patient data to a matchmaker exchange node and show patient matching with test queries.

## Purpose
This document describes how to use this app to test two different types of [Matchmaker Exchange](https://www.matchmakerexchange.org) implementations:
* [MME reference server](https://github.com/MatchmakerExchange/reference-server)
* [MatchCox](https://github.com/macarthur-lab/matchbox)

Evantually this repo will serve as a bridge to export patient data from [Scout](https://github.com/Clinical-Genomics/scout) database to a Matchmaker instance at Clinical Genomics.

## Requirements
A running instance of both [MME reference server](https://github.com/MatchmakerExchange/reference-server) server and [MatchBox](https://github.com/macarthur-lab/matchbox).
([Notes on how to install these repos](#How-to-install-MME-reference-server-and-Matchbox-on-a-local-machine))

### How to install MME reference server and Matchbox on a local machine

#### MME reference server
Follow the instructions at [this page](https://github.com/MatchmakerExchange/reference-server). Make sure to load the custom patient data from the provided [json file](https://raw.githubusercontent.com/ga4gh/mme-apis/master/testing/benchmark_patients.json).


#### MatchBox
The installation of this software via Docker is currently not working as it should and so the installation requires a workaround.

Requirements:
* Java 1.8
* Maven 3.1
* A Mongodb instance
* [Exomiser](https://github.com/exomiser/Exomiser) (read further down)

Installation steps:
* **Install Exomiser**:
This software is required for the phenotype matching algorithm of MatchBox.
1. Make sure that the following lines are present in the settings.xml file (under ~/.m2/ directory):

```sh
<settings>
  <localRepository>${user.home}/.m3/repository</localRepository>
</settings>
```

2. Clone Exomiser from github with the following command:
```sh
git clone https://github.com/exomiser/Exomiser
```

3. Change directory to the Exomiser folder and build with Maven:
```sh
mvn clean install package
```

4. Save the Exomiser phenotype data in a folder accessible by matchbox:
```sh
https://storage.googleapis.com/seqr-reference-data/1807_phenotype.tar.gz
```
and extract the data to a folder accessible by matchbox (This will be the **exomiser.data-directory** in matchbox settings).

5. Clone MatchBox from github with the following command:
```sh
git clone https://github.com/macarthur-lab/matchbox
```
and change directory to the matchbox folder.

6. Edit the configuration file src/main/resources/application.properties by filling in the following mongodb required fields:
...* spring.data.mongodb.host=127.0.0.1
...* spring.data.mongodb.port=27017
...* spring.data.mongodb.database=cgmatchbox
...* pring.data.mongodb.username=mboxuser
...* spring.data.mongodb.password=mboxpassword

and the Exomiser data directory ones:
...* exomiser.data-directory=path_to/matchbox_phenotypes
...* exomiser.phenotype.data-version=1807
