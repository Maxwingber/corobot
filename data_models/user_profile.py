# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

class PersonalData:
    def __init__(self, family_name: str = None, first_name: str = None, gender: str = None, street: str = None,\
        zipcode: str = None, city: str = None, telephone: str = None, email: str = None,\
        birthday: str = None,):
        self.family_name: str = family_name
        self.first_name: str = first_name
        self.gender: str = gender
        self.street: str = street
        self.zipcode: str = zipcode
        self.city: str = city
        self.telephone: str = telephone
        self.email: str = email
        self.birthday: str = birthday

class UserProfile:
    def __init__(
        self, age: int = 0, name: str = None, symptoms: List[str] = None, symptoms_date: str = None,\
        fever_temp: float = 0.0, critical_symptoms_bool: bool = False,\
        risk_countries_bool: bool = False, risk_countries: List[str] = None,\
        risk_country_returndate: str = None, contact_risk_1_bool: bool = False,\
        contact_risk_1_date: str = None, contact_risk_2_bool: bool = False,\
        contact_risk_2_date: str = None, contact_names: List[str] = None,\
        critical_job: str = None, risk_category: int = 0, personal_data: PersonalData = None
    ):
        self.name: str = name
        self.age: int = age
        
        self.symptoms: List[str] = symptoms
        self.symptoms_date: str = symptoms_date
        self.fever_temp: float = fever_temp
        self.critical_symptoms_bool: bool = critical_symptoms_bool      # macht vielleicht Sinn
        self.risk_countries_bool: bool = risk_countries_bool    # macht vielleicht Sinn
        self.risk_countries: List[str] = risk_countries
        self.risk_country_returndate: str = risk_country_returndate
        
        self.contact_risk_1_bool: bool = contact_risk_1_bool
        self.contact_risk_1_date: str = contact_risk_1_date
        self.contact_risk_2_bool: bool = contact_risk_2_bool
        self.contact_risk_2_date: str = contact_risk_2_date
        self.contact_names: List[str] = contact_names       # falls mans braucht
        
        self.critical_job: str = critical_job
        self.risk_category: int = risk_category   # bei 1 und 2 Aufforderung zur Personendatenabfrage

        self.personal_data: PersonalData = personal_data
