import os
import boto3
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

# Load environment variables
load_dotenv()

# AWS Configuration
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_SESSION_TOKEN = os.getenv('AWS_SESSION_TOKEN')  # For temporary credentials
BEDROCK_MODEL_ID = os.getenv('AWS_BEDROCK_MODEL_ID', 'anthropic.claude-3-sonnet-20240229-v1:0')

def get_aws_session():
    """Create AWS session with proper credential handling"""
    try:
        # Try explicit credentials first
        if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
            session = boto3.Session(
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                aws_session_token=AWS_SESSION_TOKEN,  # Optional for temporary creds
                region_name=AWS_REGION
            )
        else:
            # Fall back to default credential chain (AWS CLI, IAM roles, etc.)
            session = boto3.Session(region_name=AWS_REGION)
        
        # Test the credentials
        sts = session.client('sts')
        identity = sts.get_caller_identity()
        print(f"AWS Authentication successful! User: {identity.get('Arn', 'Unknown')}")
        return session
        
    except NoCredentialsError:
        raise Exception("AWS credentials not found. Please configure your credentials.")
    except PartialCredentialsError:
        raise Exception("Incomplete AWS credentials. Please check your configuration.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'InvalidUserID.NotFound':
            raise Exception("AWS credentials are invalid or expired.")
        else:
            raise Exception(f"AWS authentication error: {e.response['Error']['Message']}")
    except Exception as e:
        raise Exception(f"Failed to create AWS session: {str(e)}")

def validate_aws_services():
    """Validate that required AWS services are accessible"""
    session = get_aws_session()
    
    # Test Textract access
    try:
        textract = session.client('textract')
        # Try a simple operation to validate access
        textract.describe_document_text_detection(JobId='test-job-id')
    except ClientError as e:
        if e.response['Error']['Code'] in ['InvalidJobIdException', 'InvalidParameterException']:
            print("✓ Textract access confirmed")
        elif e.response['Error']['Code'] == 'AccessDeniedException':
            raise Exception("Access denied to AWS Textract. Please check your permissions.")
        else:
            print(f"⚠ Textract access check inconclusive: {e.response['Error']['Code']}")
    
    # Test Bedrock access
    try:
        bedrock = session.client('bedrock-runtime')
        # List available models to test access
        bedrock.list_foundation_models()
        print("✓ Bedrock access confirmed")
    except ClientError as e:
        if e.response['Error']['Code'] == 'AccessDeniedException':
            raise Exception("Access denied to AWS Bedrock. Please check your permissions.")
        else:
            print(f"⚠ Bedrock access check failed: {e.response['Error']['Code']}")
    
    return session

# Print configuration info
def print_config_info():
    print("AWS Configuration:")
    print(f"  Region: {AWS_REGION}")
    print(f"  Access Key: {'***' + AWS_ACCESS_KEY_ID[-4:] if AWS_ACCESS_KEY_ID else 'Not set'}")
    print(f"  Secret Key: {'Set' if AWS_SECRET_ACCESS_KEY else 'Not set'}")
    print(f"  Session Token: {'Set' if AWS_SESSION_TOKEN else 'Not set'}")
    print(f"  Bedrock Model: {BEDROCK_MODEL_ID}")

if __name__ == "__main__":
    print_config_info()
    try:
        validate_aws_services()
        print("✓ All AWS services are accessible!")
    except Exception as e:
        print(f"✗ AWS setup issue: {e}")
