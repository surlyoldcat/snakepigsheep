# snakepigsheep
This is a set of utilities which extracts OpenAPI/swagger from existing API Gateway APIs and publishes them to a static site, using swagger-ui to generate UI.

Swagger Sites
- [Active](http://active-platform-swaggerpub.s3-website-us-east-1.amazonaws.com)
- QA (TBD)

## publish_site
This utility will create or update a static site in S3 which contains multiple swagger-ui subsites, one per API. It also creates a very basic root index with links to each API subsite.

The API Gateway swagger is saved in each subsite as `exported-swagger.json`

The site layout is:
```
(s3 root)
--- index.html
--- subscriptions
------ swagger-ui files
------ exported-swagger.json
--- curriculum
------ swagger-ui files
------ exported-swagger.json
--- other api
------ ...
```

The config for the tool is stored in `config.json`:
```
{
  "publish_bucket": "active-platform-swaggerpub",  // name of S3 bucket you created, set up to publish a static website
  "aws_profile": "active",  // name of a AWS profile in your local credentials file
  "output_dir": "pub",  // this directory gets synced to S3
  "apis": [
    {
      "id": "mh3ueqlih0", // this can most easily by found in the Search list for API Gatewaay 
      "name": "subscriptions", 
      "stage": "active"
    },
    {
      "id": "8ohhklieya",
      "name": "user_service_lambdas",
      "stage": "active"
    },
     {
      "id": "foo123",
      "name": "myfancyAPI",
      "stage": "active"
    },
  ]
}
```

To find the URL for the S3 website, go to the bucket in AWS Console, click the Properties tab, and scroll all the way to the bottom.
For the active-platform-swaggerpub bucket, the URL is http://active-platform-swaggerpub.s3-website-us-east-1.amazonaws.com

## update_api
Updates the published swagger for a single API. Uses the same logic as publish_site, except it only cares about exported-swagger.json. It requires the larger site to already be published.

Usage: `python3 update_api.py 8ohhklieya`

NOT YET COMPLETE

# TODO
- add utility to update the swagger for a single API/stage
- add a utility to publish APIG documentation (https://stackoverflow.com/questions/43238034/documentation-specified-in-open-api-does-not-export-from-aws-api-gateway)
- add a build trigger to update swagger when QA is deployed (per repo)