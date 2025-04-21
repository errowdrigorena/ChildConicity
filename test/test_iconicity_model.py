import pytest
from src.iconicity_model import IconicityModel

@pytest.fixture
def sample_data():
    return {
        1: {
            'word': 'casa',
            'n_ratings': 10,
            'n': 15,
            'prop_knwn': 0.8,
            'rating': 4.5,
            'rating_sd': 1.2
        },
        2: {
            'word': 'perro',
            'n_ratings': 12,
            'n': 15,
            'prop_knwn': 0.9,
            'rating': 3.8,
            'rating_sd': 1.0
        },
        3: {
            'word': 'gato',
            'n_ratings': 8,
            'n': 15,
            'prop_knwn': 0.7,
            'rating': 4.2,
            'rating_sd': 1.1
        }
    }

@pytest.fixture
def model(sample_data):
    return IconicityModel(sample_data)

def test_initialization(model):
    assert len(model.word_data) == 3
    assert 'casa' in model.word_data
    assert 'perro' in model.word_data
    assert 'gato' in model.word_data

def test_get_word_data(model):
    casa_data = model.get_word_data('casa')
    assert casa_data is not None
    assert casa_data['n_ratings'] == 10
    assert casa_data['rating'] == 4.5
    assert casa_data['prop_knwn'] == 0.8

def test_get_all_words(model):
    words = model.get_all_words()
    assert len(words) == 3
    assert 'casa' in words
    assert 'perro' in words
    assert 'gato' in words

def test_get_words_by_rating(model):
    # Palabras con rating >= 4.0
    high_rating_words = model.get_words_by_rating(min_rating=4.0)
    assert len(high_rating_words) == 2
    assert 'casa' in high_rating_words
    assert 'gato' in high_rating_words
    
    # Palabras con rating entre 3.5 y 4.0
    mid_rating_words = model.get_words_by_rating(min_rating=3.5, max_rating=4.0)
    assert len(mid_rating_words) == 1
    assert 'perro' in mid_rating_words

def test_get_words_by_known_proportion(model):
    # Palabras con prop_knwn >= 0.8
    high_prop_words = model.get_words_by_known_proportion(min_prop=0.8)
    assert len(high_prop_words) == 2
    assert 'casa' in high_prop_words
    assert 'perro' in high_prop_words
    
    # Palabras con prop_knwn <= 0.8
    low_prop_words = model.get_words_by_known_proportion(max_prop=0.8)
    assert len(low_prop_words) == 2
    assert 'casa' in low_prop_words
    assert 'gato' in low_prop_words

def test_invalid_word(model):
    assert model.get_word_data('nonexistent') is None 