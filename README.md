## RabbitMQ Data Processing Application Prototype

This application demonstrates how to use RabbitMQ to process edit events and perform aggregations on them.

### Setup

1. **Ensure you have Docker and Docker Compose installed on your system.**  

2. **Clone this repository to your local machine.**


### Running the Application

1. **Open a terminal and navigate to the project directory, then run:.**

   ```bash
   docker-compose up
   ```
   
you will see the three containers running, rabbitmq instance, producer and consumer. The results will be calculated and logged. By the end data will be fetched to ``results.json`` in consumer container.

### Assumptions 

1. **For the sake of prototype the data is stored as an array of documents in file called "results.json" to get the data, use docker cp command and get the file from consumer's container like this:**

```commandline
docker cp rabbitmq_prototype_consumer:/app/results.json .
```   

2. **A flag is published by producer (b'END') to notify the end of messages and therefore dumping the results**
3. That approach was for the sake of prototype in production there shall be no-sql database to store the results, which would be suitable for querying and dashboards.


## Questions

1. A timeseries database to store the monitoring data for dashboards or a document based database like redis could be suitable for the usecase.

**Advantages:**

**Scalable:** can scale horizontally making it suitable for handling large amount of data.

**Performance:** concurrent reads and writes effeciently.

**Cons**

Doesn't conform with typical SQL database properties(ACID). 



2. **Data model:**  Document based model, as more fields can be added in the future, and given the data is semi-structured, flexible schema and can be suitable for various event structures.  


3. Direct exchange 

**Pros:**  
1.Simple and efficient.  
2.Ideal for point-to-point communication.  
3.Suitable for simple routing based on exact routing keys.  
**Cons:**  
1.Limited routing flexibility compared to other exchange types.  
2.Might not be optimal if you need more advanced routing patterns.  
3.Scalability and fault tolerance wise direct exchange may be not the strongest, if queue goes down messages can be lost and additional mechanism shall be implemented to avoid that. 