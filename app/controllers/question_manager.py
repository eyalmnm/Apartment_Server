import json

from flask import jsonify
from app.utils.uuid_utils import generate_uuid

# Question Id will be used by UUID insteadof number
# temp_uuid = generate_uuid()