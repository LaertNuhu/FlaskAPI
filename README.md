# FlaskAPI
This application can provide data which can be used by a application that uses D3.js to create force directed graph

**Hosted on Heroku**

# API Endpoints
**ROOT URL:** `https://med-data-visualisation.herokuapp.com/`

#### GetNodesByCount
* **URL:** `/count/[threshold]/`

* **Description**: Get the output of CountVectorizer

* **Method:** `GET`
  
*  **URL Params**

   * **Optional:**
 
       `groups=[alpha]` : `y - get groups` 
   
       `centrality=[alpha]` : `d - degree, c - closeness`

* **Success Response:**
    
    In case groups=y and centrality=d
  
  * **Code:** 200 <br />
    **Content:** `{
"directed": false,
"multigraph": false,
"graph": {},
"nodes": [
{
"degree_centrality": 0.18623232944068838,
"group": 1,
"id": "year"
}, ... ]
"links": [
{ 
"Weight": 8, 
"source": "year", 
"target": "old" 
},
... ] }`


#### GetNodesByTfidf
* **URL:** `/tfidf/[threshold]/`

* **Description**: Get the output of TfidfVectorizer

* **Method:** `GET`
  
*  **URL Params**

   * **Optional:**
 
       `groups=[alpha]` : `y - get groups` 
   
       `centrality=[alpha]` : `d - degree, c - closeness`

* **Success Response:**
    
    In case groups=y and centrality=d
  
  * **Code:** 200 <br />
    **Content:** `{
"directed": false,
"multigraph": false,
"graph": {},
"nodes": [
{
"degree_centrality": 0.02586206896551724,
"group": 1,
"id": "year"
}, ... ]
"links": [
{ 
"Weight": 1.8841617785876779, 
"source": "year", 
"target": "old" 
},
... ] }`


#### GetSkipgramsByCount
* **URL:** `/tfidf/[threshold]/`

* **Description**: Get the output of CountVectorizer using Skipgramms

* **Method:** `GET`
  
*  **URL Params**

   * **Optional:**
 
       `groups=[alpha]` : `y - get groups` 
   
       `centrality=[alpha]` : `d - degree, c - closeness`
       
       `window_size=[number]`

* **Success Response:**
    
    In case groups=y and centrality=d
  
  * **Code:** 200 <br />
    **Content:** `{
"directed": false,
"multigraph": false,
"graph": {},
"nodes": [
{
"degree_centrality": 0.02586206896551724,
"group": 1,
"id": "year"
}, ... ]
"links": [
{ 
"Weight": 1.8841617785876779, 
"source": "year", 
"target": "old" 
},
... ] }`


#### GetSkipgramsByTfidf
* **URL:** `/tfidf/[threshold]/`

* **Description**: Get the output of TfidfVectorizer using Skipgramms

* **Method:** `GET`
  
*  **URL Params**

   * **Optional:**
 
       `groups=[alpha]` : `y - get groups` 
   
       `centrality=[alpha]` : `d - degree, c - closeness`
       
       `window_size=[number]`

* **Success Response:**
    
    In case groups=y and centrality=d
  
  * **Code:** 200 <br />
    **Content:** `{
"directed": false,
"multigraph": false,
"graph": {},
"nodes": [
{
"degree_centrality": 0.02586206896551724,
"group": 1,
"id": "year"
}, ... ]
"links": [
{ 
"Weight": 1.8841617785876779, 
"source": "year", 
"target": "old" 
},
... ] }`
