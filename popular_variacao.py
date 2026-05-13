import os
import django
import cloudinary.api

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projeto.settings")
django.setup()


cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

from core.models import VariacaoExercicio

# Busca todos os gifs do Cloudinary
resultado = cloudinary.api.resources(
    type="upload",
    prefix="media/gifs/",
    resource_type="image",
    max_results=500
)

variacoes = VariacaoExercicio.objects.all()

for item in resultado["resources"]:

    public_id = item["public_id"]

    # Ex:
    # media/gifs/Agachamento_Frontal_abcd123
    nome_gif = public_id.split("/")[-1]

    nome_limpo = (
        nome_gif
        .split("_")[0]
        .replace("-", " ")
        .lower()
        .strip()
    )

    print(f"\nGIF encontrado: {nome_gif}")

    encontrou = False

    for variacao in variacoes:

        nome_variacao = variacao.nome.lower().strip()

        if nome_variacao in nome_gif.lower():

            # salva o caminho cloudinary
            variacao.gif = item["secure_url"]
            variacao.save()

            print(f"OK -> {variacao.nome}")

            encontrou = True
            break

    if not encontrou:
        print("NÃO ASSOCIADO")