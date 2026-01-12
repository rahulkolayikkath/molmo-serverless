# molmo-serverless
Serverless deployment of molmo on Runpod

### Steps 
1. Create a docket image from the dockerfile atatched and push it to dockerhub 
2. Go to Runpod-> serverless -> new endpoint
3. import from docker registry 
4. Endpoint type : Queue, Worker type : GPU 
5. GPU configuration : 48 GB ( A600, A40 will be assigned which is enough)
6. Container Configuration -> container disk volume 60 GB , expose portt 8080,8000. Slect Deploy endpoint 
7. Test this after the endpoint is ready using requests from console
8. Copy the Endpoint ID and also creat a api key to use it in our env variables.