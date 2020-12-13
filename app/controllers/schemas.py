from marshmallow import Schema, fields, validate


# ==================================   User  ==================================
class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    company_uuid = fields.Str(required=True)


class RegistrationSchema(Schema):
    uuid = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    language = fields.Str(required=False)
    status = fields.Int(required=True, validate=[validate.OneOf([1, 2, 5, 10])])
    email = fields.Str(required=True)
    phone = fields.Str(required=True)
    company_uuid = fields.Str(required=True)


class TheAdminLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


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


class AddNewEntranceSchema(Schema):
    uuid = fields.Str(required=True)
    building_id = fields.Int(required=True)
    name = fields.Int(required=True)


class GetEntranceByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class UpdateEntranceByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)
    building_id = fields.Int(required=True)
    name = fields.Int(required=True)


class DeleteEntranceByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class AddNewFloorSchema(Schema):
    uuid = fields.Str(required=True)
    entrance_id = fields.Int(required=True)
    name = fields.Int(required=True)


class GetFloorByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class UpdateFloorByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)
    entrance_id = fields.Int(required=True)
    name = fields.Int(required=True)


class DeleteFloorByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class AddNewApartmentSchema(Schema):
    uuid = fields.Str(required=True)
    floor_id = fields.Int(required=True)
    company_id = fields.Int(required=True)
    name = fields.Int(required=True)


class GetApartmentByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class UpdateApartmentByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)
    floor_id = fields.Int(required=True)
    company_id = fields.Int(required=True)
    name = fields.Int(required=True)


class DeleteApartmentByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class AddNewRoomSchema(Schema):
    uuid = fields.Str(required=True)
    name = fields.Str(required=True)
    type = fields.Int(required=True)
    apartment_id = fields.Int(required=True)


class GetRoomByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class UpdateRoomByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    type = fields.Int(required=True)
    apartment_id = fields.Int(required=True)


class DeleteRoomByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Int(required=True)


class AddNewQuestionnaireSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    room_id = fields.Int(required=True)


class GetQuestionnaireByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)


class UpdateQuestionnaireByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    room_id = fields.Int(required=True)


class DeleteQuestionnaireByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)


class AddNewQuestionSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)
    type = fields.Int(required=True)
    text = fields.Str(required=True)
    questionnaire_id = fields.Str(required=True)


class GetQuestionByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)


class UpdateQuestionByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)
    type = fields.Int(required=True)
    text = fields.Str(required=True)
    questionnaire_id = fields.Str(required=True)


class DeleteQuestionByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)


class AddNewAnswerSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)
    text = fields.Str(required=True)
    question_id = fields.Str(required=True)


class GetAnswerByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)


class UpdateAnswerByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)
    text = fields.Str(required=True)
    question_id = fields.Str(required=True)


class DeleteAnswerByIdSchema(Schema):
    uuid = fields.Str(required=True)
    id = fields.Str(required=True)


class AddNewAnalyticsSchema(Schema):
    uuid = fields.Str(required=True)
    event = fields.Int(required=True)
    data = fields.Str(required=True)
