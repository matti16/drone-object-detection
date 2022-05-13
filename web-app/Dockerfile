FROM 568480506324.dkr.ecr.eu-west-1.amazonaws.com/lambda/python:3.8

# Copy function code
COPY src/ ${LAMBDA_TASK_ROOT}

# Install the function's dependencies using file requirements.txt
# from your project folder.

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"