import pandas as pd
import numpy as np
import streamlit as st
import pickle,gzip

import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=a20271b3f5ef76ced6f3175923149c08&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+ data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    if isinstance(similarity,np.ndarray):
         distances = similarity[movie_index]
    else:
        distances = similarity.toarray()[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters =[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        #fetching movie using api
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetching movies poster using api
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_posters


movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(gzip.open('movies_similarity.pkl.gz','rb'))

st.title('Movie Recommender System')

#making search bar
selected_movie_name= st.selectbox(
    'Choose a Movie name to get related other movies?',
    movies['title'].values)

if st.button("Recommend"):
    names,posters = recommend(selected_movie_name)
    col1 , col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])