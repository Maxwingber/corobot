# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List


class UserProfile:
    def __init__(
        self, name: str = None, age: int = 0, gender: str = None, street: str = None,\
        plz: int = 0, city: str = None, telephone: str = None, email: str = None,\
        birthday: str = None, symptoms: List[str] = None, symptoms_date: str = None,\
        fever_temp: float = 0.0, critical_symptoms_bool: bool = False,\
        risk_countries_bool: bool = False, risk_countries: List[str] = None,\
        risk_country_returndate: str = None, contact_risk_1_bool: bool = False,\
        contact_risk_1_date: str = None, contact_risk_2_bool: bool = False,\
        contact_risk_2_date: str = None, contact_names: List[str] = None,\
        critical_job: str = None, risk_category: int = 0
    ):
        self.name: str = name
        self.age: int = age
        self.gender: str = gender
        self.street: str = street
        self.plz: int = plz
        self.city: str = city
        self.telephone: str = telephone
        self.email: str = email
        self.birthday: str = birthday
        
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
        self.risk_category: int = risk_category           # bei 1 und 2 Aufforderung zur Personendatenabfrage