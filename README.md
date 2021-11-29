# traefik-mockoon
Traefik HTTP provider for Mockoon CLI

## Problem statement

Mockoon is used for creating API Mock services. It have server side component called Mockoon-cli which is used to deploy and run API Mock services.

In Mockoon-cli, every Mock service runs with own port. If we have 100 API microservices then we may need to create 100 Mock services and all these 100 mock services runs on own TCP port (3000, 3001,..3100).

Example, If we have 100 Mock services,

    ```
    http://mockoon-cli1:3001/api/mock1
    http://mockoon-cli1:3002/api/mock2
    ......
    http://mockoon-cli1:3100/api/mock100
    ```

Its very difficult to maintain many Mock services across many ports. If we want to utilize a mock service mock1 in our frontend applications then we need to check first to find where the mock1 mock service running and its port number.

Also If we want to use a load balancer in front of Mockoon-cli, then we need to update the load balancer configuration file manually whenever new mock service is deployed in Mockoon-cli and its tedious process.
