from marshmallow import Schema, fields, validate


# ==================================   User  ==================================
class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    company_id = fields.Str(required=True)


class RegistrationSchema(Schema):
    uuid = fields.Str(required=True)
    username = fields.Str(required=True)
    password_hash = fields.Str(required=True)
    salt = fields.Str(required=True)
    language = fields.Str(required=False)
    status = fields.Int(required=True, validate=[validate.OneOf([1, 2, 5, 10])])
    email = fields.Str(required=True)
    phone = fields.Str(required=True)
    company_id = fields.Str(required=True)


# ==================================   Company  ===============================
class RegisterNewCompanySchema(Schema):
    uuid = fields.Str(required=True)
    name = fields.Str(required=True)
    registration_id = fields.Str(required=True)
    address = fields.Str(required=True)
    city = fields.Str(required=True)
    state = fields.Str(required=False)
    country = fields.Str(required=True)
    zip_code = fields.Int(required=True)
    phone = fields.Str(required=True)
    # status = fields.Int(required=True, validate=[validate.OneOf([1, 2, -1])])


class RegisterNewSubCompanySchema(Schema):
    uuid = fields.Str(required=True)
    name = fields.Str(required=True)
    registration_id = fields.Str(required=True)
    parent_company_id = fields.Str(required=True)
    address = fields.Str(required=True)
    city = fields.Str(required=True)
    state = fields.Str(required=False)
    country = fields.Str(required=True)
    zip_code = fields.Int(required=True)
    phone = fields.Str(required=True)
    # status = fields.Int(required=True, validate=[validate.OneOf([1, 2, -1])])


class GetCompanyIyIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class UpdateCompanyByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    registration_id = fields.Str(required=True)
    parent_company_id = fields.Str(required=True)
    address = fields.Str(required=True)
    city = fields.Str(required=True)
    state = fields.Str(required=False)
    country = fields.Str(required=True)
    zip_code = fields.Int(required=True)
    phone = fields.Str(required=True)


class DeleteCompanyByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class AddNewCountrySchema(Schema):
    uuid = fields.Str(required=True)
    name = fields.Str(required=True)


class GetCountryByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class UpdateCountryByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    name = fields.Str(required=True)


class DeleteCountryByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class AddNewStateSchema(Schema):
    uuid = fields.Str(required=True)
    country_id = fields.Int(required=True)
    name = fields.Str(required=True)


class GetStateByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class UpdateStateByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    country_id = fields.Int(required=True)
    name = fields.Str(required=True)


class DeleteStateByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class AddNewCitySchema(Schema):
    uuid = fields.Str(required=True)
    state_id = fields.Int(required=True)
    name = fields.Str(required=True)


class GetCityByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class UpdateCityByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    state_id = fields.Int(required=True)
    name = fields.Str(required=True)


class DeleteCityByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class AddNewStreetSchema(Schema):
    uuid = fields.Str(required=True)
    city_id = fields.Int(required=True)
    name = fields.Str(required=True)


class GetStreetByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class UpdateStreetByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    city_id = fields.Int(required=True)
    name = fields.Str(required=True)


class DeleteStreetByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class AddNewBuildingSchema(Schema):
    uuid = fields.Str(required=True)
    street_id = fields.Int(required=True)
    company_id = fields.Int(required=True)
    name = fields.Str(required=True)


class GetBuildingByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class UpdateBuildingByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    street_id = fields.Int(required=True)
    company_id = fields.Int(required=True)
    name = fields.Str(required=True)


class DeleteBuildingByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
