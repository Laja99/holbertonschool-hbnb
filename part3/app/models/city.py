from app.extensions import db

from app.models.base_model import BaseModel



class City(BaseModel):

    __tablename__ = 'cities'



    name = db.Column(db.String(100), nullable=False)

 



    def __init__(self, name, **kwargs):

        super().__init__(**kwargs)

        if not name:

            raise ValueError("City name is required")

        self.name = name



    def to_dict(self):

        data = super().to_dict()

        data.update({

            "name": self.name

        })

        return data
