import pytest
from src.word_dictionary_merger import WordDictionaryMerger

@pytest.fixture
def merger():
    return WordDictionaryMerger()

@pytest.fixture
def sample_dictionaries():
    return [
        {
            'casa': {'n_ratings': 10, 'rating': 4.5},
            'perro': {'n_ratings': 12, 'rating': 3.8},
            'gato': {'n_ratings': 8, 'rating': 4.2}
        },
        {
            'casa': {'prop_known': 0.8, 'rating_sd': 1.2},
            'perro': {'prop_known': 0.9, 'rating_sd': 1.0},
            'mesa': {'prop_known': 0.7, 'rating_sd': 1.1}
        },
        {
            'casa': {'frequency': 100, 'length': 4},
            'perro': {'frequency': 80, 'length': 5},
            'silla': {'frequency': 60, 'length': 5}
        }
    ]

def test_initialization(merger):
    assert len(merger.dictionaries) == 0

def test_add_dictionary(merger, sample_dictionaries):
    merger.add_dictionary(sample_dictionaries[0])
    assert len(merger.dictionaries) == 1
    assert merger.dictionaries[0] == sample_dictionaries[0]

def test_add_invalid_dictionary(merger):
    with pytest.raises(ValueError):
        merger.add_dictionary("not_a_dictionary")

def test_obtain_merge_empty(merger):
    merged, unmerged = merger.obtain_merge()
    assert merged == {}
    assert unmerged == []

def test_obtain_merge(merger, sample_dictionaries):
    for dictionary in sample_dictionaries:
        merger.add_dictionary(dictionary)
    
    merged, unmerged = merger.obtain_merge()
    
    # Verificar palabras comunes (casa y perro)
    assert 'casa' in merged
    assert 'perro' in merged
    assert 'gato' not in merged
    assert 'mesa' not in merged
    assert 'silla' not in merged
    
    # Verificar datos mergeados
    assert merged['casa'] == {
        'n_ratings': 10,
        'rating': 4.5,
        'prop_known': 0.8,
        'rating_sd': 1.2,
        'frequency': 100,
        'length': 4
    }
    
    # Verificar diccionarios no mergeados
    assert len(unmerged) == 3
    assert 'gato' in unmerged[0]
    assert 'mesa' in unmerged[1]
    assert 'silla' in unmerged[2] 