FROM openjdk:17-slim

WORKDIR /app

# Download the RMLMapper JAR file
ADD https://github.com/RMLio/rmlmapper-java/releases/download/v7.2.0/rmlmapper-7.2.0-r374-all.jar /app/rmlmapper.jar

# Add the mapping file to the image
COPY mapping.rml.ttl /app/mapping.rml.ttl

# Add the input file to the image (optional)
COPY data.xml /app/data.xml

ENTRYPOINT ["java", "-jar", "/app/rmlmapper.jar"]
