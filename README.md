# PCF + GCP Retail Demo

![Diagram showing major components and how data flows](./images/data_flow_diagram.png)

## A demo for retailers to see how PCF and GCP turn streams of data into action. 

## Prerequisites
* Install the GCP Service Broker, available on [GitHub](https://github.com/GoogleCloudPlatform/gcp-service-broker)
or [Pivotal Network](https://network.pivotal.io/products/gcp-service-broker/)
* Java 8 JDK installed
* [Git client](https://git-scm.com/downloads) installed
* Build a fork of the [Spring Cloud Stream Binder for Google PubSub](https://github.com/mgoddard-pivotal/spring-cloud-stream-binder-google-pubsub) project:
    - Clone the repo: `$ git clone https://github.com/mgoddard-pivotal/spring-cloud-stream-binder-google-pubsub.git`
    - Change into the new directory: `$ cd spring-cloud-stream-binder-google-pubsub/`
    - Build and install the JAR: `$ bash ./mvnw -U clean install`

## Initial Phase: deploy a simple stream with Source, Processor, and Sink
As a proof that we can deploy a stream using Google PubSub, we can deploy the classic Time => Log steam
with a Processor in between.

1. Build the Spring Boot JAR files: `for project in ./time-source/ ./transform-proc/ ./log-sink/ ; do ( cd $project && ./mvnw clean package -DskipTests ) ; done`
1. Create a PubSub service instance: `cf cs google-pubsub default pubsub`
1. Run a script to push the three Boot apps, bind to pubsub, and start them: `./scripts/scdf_source_proc_sink.sh`

You will see the logs scrolling by as the app is deployed, bound, started.  Once that finishes, you can
look at the logs for the log-sink app, to see if entries occur every second, when the time-source emits
them: `cf logs log-sink`



## Resources
* [Document showing how to create Spring Cloud Stream components bound to Google PubSub](./docs/GooglePubSubBinderandSCDF.pdf)
* [Spring Initializr for Stream Apps](http://start-scs.cfapps.io/)
* [Spring Cloud Dataflow Server](https://storage.googleapis.com/mgoddard-jars/spring-cloud-dataflow-server-cloudfoundry-1.1.1.BUILD-SNAPSHOT.jar),
  with changes to specify Google Cloud role during bind. That version of the SCDF Server JAR was built
  with a patched version of
  [Spring Cloud Deployer for Cloud Foundry](https://github.com/spring-cloud/spring-cloud-deployer-cloudfoundry), 
  to specify the Google Cloud role at bind time. The CloudFoundryAppDeployer.java file was modified:

```
  private Mono<Void> requestBindService(String deploymentId, String service) {
    return this.operations.services()
      .bind(BindServiceInstanceRequest.builder()
      .parameter("role", "pubsub.admin") // This was added
      .applicationName(deploymentId)
      .serviceInstanceName(service)
      .build());
  }
```

