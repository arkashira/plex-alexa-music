# Dataflow Architecture
## Overview
The plex-alexa-music skill enables voice control of personal music libraries stored on Plex or Emby through Alexa devices. The following dataflow architecture outlines the system's components and interactions.

## External Data Sources
```
                                  +---------------+
                                  |  Plex/Emby   |
                                  |  Music Library|
                                  +---------------+
```
* Plex/Emby music library APIs

## Ingestion Layer
```
                                  +---------------+
                                  |  Plex/Emby   |
                                  |  Music Library|
                                  +---------------+
                                            |
                                            |
                                            v
                                  +---------------+
                                  |  API Gateway  |
                                  |  (AuthN/Z, SSL) |
                                  +---------------+
                                            |
                                            |
                                            v
                                  +---------------+
                                  |  Data Ingestor |
                                  |  (Plex/Emby API) |
                                  +---------------+
```
* API Gateway (AuthN/Z, SSL)
* Data Ingestor (Plex/Emby API)

## Processing/Transform Layer
```
                                  +---------------+
                                  |  Data Ingestor |
                                  |  (Plex/Emby API) |
                                  +---------------+
                                            |
                                            |
                                            v
                                  +---------------+
                                  |  Data Processor|
                                  |  (Metadata Extraction)|
                                  +---------------+
                                            |
                                            |
                                            v
                                  +---------------+
                                  |  Data Transformer|
                                  |  (Format Conversion) |
                                  +---------------+
```
* Data Processor (Metadata Extraction)
* Data Transformer (Format Conversion)

## Storage Tier
```
                                  +---------------+
                                  |  Data Transformer|
                                  |  (Format Conversion) |
                                  +---------------+
                                            |
                                            |
                                            v
                                  +---------------+
                                  |  Database (Metadata) |
                                  |  (AuthN/Z, Encryption) |
                                  +---------------+
                                            |
                                            |
                                            v
                                  +---------------+
                                  |  File Storage (Music) |
                                  |  (AuthN/Z, Encryption) |
                                  +---------------+
```
* Database (Metadata) (AuthN/Z, Encryption)
* File Storage (Music) (AuthN/Z, Encryption)

## Query/Serving Layer
```
                                  +---------------+
                                  |  Database (Metadata) |
                                  |  (AuthN/Z, Encryption) |
                                  +---------------+
                                            |
                                            |
                                            v
                                  +---------------+
                                  |  Query Service    |
                                  |  (Metadata Retrieval) |
                                  +---------------+
                                            |
                                            |
                                            v
                                  +---------------+
                                  |  Alexa Skill API  |
                                  |  (Voice Control Interface) |
                                  +---------------+
```
* Query Service (Metadata Retrieval)
* Alexa Skill API (Voice Control Interface)

## Egress to User
```
                                  +---------------+
                                  |  Alexa Skill API  |
                                  |  (Voice Control Interface) |
                                  +---------------+
                                            |
                                            |
                                            v
                                  +---------------+
                                  |  Alexa Device   |
                                  |  (Voice Output)    |
                                  +---------------+
```
* Alexa Device (Voice Output)

## Auth Boundaries
* API Gateway (AuthN/Z, SSL)
* Database (Metadata) (AuthN/Z, Encryption)
* File Storage (Music) (AuthN/Z, Encryption)
* Alexa Skill API (Voice Control Interface) (AuthN/Z, SSL)