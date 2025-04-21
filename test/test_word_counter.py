import pytest
from src.word_counter import WordCounter

@pytest.fixture
def word_counter():
    return WordCounter()

def test_count_words(word_counter):
    # Datos de prueba
    test_data = {
        1: {'text': 'hola mundo hola'},
        2: {'text': 'mundo python'},
        3: {'text': 'hola python'}
    }
    
    # Contar palabras
    counts = word_counter.count_words(test_data)
    
    # Verificar resultados
    assert counts['hola'] == 3
    assert counts['mundo'] == 2
    assert counts['python'] == 2
    assert len(counts) == 3

def test_empty_data(word_counter):
    # Datos vacíos
    test_data = {}
    
    # Contar palabras
    counts = word_counter.count_words(test_data)
    
    # Verificar resultados
    assert len(counts) == 0

def test_no_text_field(word_counter):
    # Datos sin campo 'text'
    test_data = {
        1: {'other': 'hola'},
        2: {'other': 'mundo'}
    }
    
    # Contar palabras
    counts = word_counter.count_words(test_data)
    
    # Verificar resultados
    assert len(counts) == 0

def test_get_most_common(word_counter):
    # Datos de prueba
    test_data = {
        1: {'text': 'hola mundo hola'},
        2: {'text': 'mundo python'},
        3: {'text': 'hola python'}
    }
    
    # Contar palabras
    word_counter.count_words(test_data)
    
    # Obtener las 2 palabras más comunes
    most_common = word_counter.get_most_common(2)
    
    # Verificar resultados
    assert len(most_common) == 2
    assert most_common[0] == ('hola', 3)
    assert most_common[1] == ('mundo', 2)

def test_case_insensitive(word_counter):
    # Datos con diferentes mayúsculas/minúsculas
    test_data = {
        1: {'text': 'Hola MUNDO hola'},
        2: {'text': 'mundo Python'}
    }
    
    # Contar palabras
    counts = word_counter.count_words(test_data)
    
    # Verificar resultados
    assert counts['hola'] == 2
    assert counts['mundo'] == 2
    assert counts['python'] == 1 