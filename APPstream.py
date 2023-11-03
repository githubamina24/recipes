#!/usr/bin/env python
# coding: utf-8

# In[ ]:
#pip install word2vec_Rec
#import word2vec_Rec
import streamlit as st
from PIL import Image
from SessionState import SessionState
import pandas as pd
import nltk
import altair as alt
from altair import Chart
from streamlit.report_thread import ReportThread
import config, rec_sys
from ingredient_parser import ingredient_parser
import word2vec_rec
from word2vec_rec import get_recs


# If you use NLTK, download the required data
try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")

# Define the function to make clickable links
def make_clickable(name, link):
    text = name
    return f'<a target="_blank" href="{link}">{text}</a>'

# Replace with the actual link to your image
# image_link = "https://images.app.goo.gl/6oDJ4XPXDtt5VDx46"
def main():
    st.markdown("# *Recipe Recommendation System*")

    st.markdown(
        "Machine Learning powered app based on content based filtering",
        unsafe_allow_html=True,
    )

    st.markdown(
        "## Mention the ingredients you want to use in your meal!! "
    )

    st.markdown(
        " got some interesting and lazy ingredients in your kitchen lying around wondering what to make?? No worries we got your back :arrow_down:"
    )

    st.text("")


    # Create an instance of SessionState and set initial values for session-specific variables
    session_state = SessionState(
        recipe_df="",
        recipes="",
        model_computed=False,
        execute_recsys=False,
        recipe_df_clean=""
    )

    # Rest of your code
    ingredients = st.text_input(
        "Enter ingredients you would like to cook with (separate ingredients with a comma)",
        "cheese, tomato, flour",
    )
    session_state.execute_recsys = st.button("Give me recommendations!")
    
    if session_state.execute_recsys:

        col1, col2, col3 = st.columns([1, 6, 1])
        #recipe = rec_sys.RecSys(ingredients)
        recipe = get_recs(ingredients, mean=True)
        #gif_runner.empty()
        session_state.recipe_df_clean = recipe.copy()
        # link is the column with hyperlinks
        recipe["url"] = recipe.apply(
            lambda row: make_clickable(row["recipe"], row["url"]), axis=1
        )
        recipe_display = recipe[["recipe", "ingredients"]]
        session_state.recipe_display = recipe_display.to_html(escape=False)
        session_state.recipes = recipe.recipe.values.tolist()
        session_state.model_computed = True
        session_state.execute_recsys = False
       
    if session_state.model_computed:
        # st.write("Either pick a particular recipe or see the top 5 recommendations.")
        recipe_all_box = st.selectbox(
            "the top 5 recommendations",
            ["Show me them all!", "Select a single recipe"],
        )
        if recipe_all_box == "Show me them all!":
            st.write(session_state.recipe_display, unsafe_allow_html=True)
        else:
            selection = st.selectbox(
                "Select a delicious recipe", options=session_state.recipes
            )
            st.markdown(f"# {selection_details.recipe.values[0]}")
            st.subheader(f"Website: {selection_details.url.values[0]}")
            ingredients_disp = selection_details.ingredients.values[0].split(",")

            st.subheader("Ingredients:")
            col1, col2 = st.columns(2)
            ingredients_disp = [
                ingred
                for ingred in ingredients_disp
                if ingred
                not in [
                    " skin off",
                    " bone out",
                    " from sustainable sources",
                    " minced",
                ]
            ]
            ingredients_disp1 = ingredients_disp[len(ingredients_disp) // 2 :]
            ingredients_disp2 = ingredients_disp[: len(ingredients_disp) // 2]
            for ingred in ingredients_disp1:
                col1.markdown(f"* {ingred}")
            for ingred in ingredients_disp2:
                col2.markdown(f"* {ingred}")
            # st.write(f"Score: {selection_details.score.values[0]}")
            
if __name__ == "__main__":
    main()
