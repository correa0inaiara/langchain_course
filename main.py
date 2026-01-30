import pet_name_generator as png
import streamlit as st

st.title("Pets name generator")

user_animal_type = st.sidebar.selectbox("What is your pet?", ("Cat", "Dog", "Cow", "Hamster"))

# user_pet_color = ""

# animal_translation = {
#     "Cat": "um gato",
#     "Dog": "um cachorro", 
#     "Cow": "uma vaca",
#     "Hamster": "um hamster"
# }

# animal_type_for_prompt = animal_translation.get(user_animal_type, user_animal_type)

if user_animal_type == "Cat":
    user_pet_color = st.sidebar.text_area("What color is your cat?", max_chars=50)
    
if user_animal_type == "Dog":
    user_pet_color = st.sidebar.text_area("What color is your dog?", max_chars=50)
    
if user_animal_type == "Cow":
    user_pet_color = st.sidebar.text_area("What color is your cow?", max_chars=50)
    
if user_animal_type == "Hamster":
    user_pet_color = st.sidebar.text_area("What color is your hamster?", max_chars=50)
    
if user_pet_color:
    response = png.generate_pet_name(animal_type=user_animal_type, pet_color=user_pet_color)
    st.subheader("Suggested names:")
    st.write(response['pet_name'])