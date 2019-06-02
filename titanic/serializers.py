from rest_framework import serializers
from titanic.models import Titanic
class TitanicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Titanic
        fields = ('PassengerId',     'Pclass',    'Name' ,   'Sex' ,   'Age' ,   'SibSp',    'Parch',    'Ticket',    'Fare',    'Cabin',    'Embarked')
