from django import forms


# Форма для добавления сделки
class AddDeal(forms.Form):
    title = forms.CharField(label="Название", max_length=100)
    sum = forms.FloatField(label="Сумма", min_value=0)
    probability = forms.IntegerField(label="Вероятность завершения сделки в срок (%)", min_value=0, max_value=100)