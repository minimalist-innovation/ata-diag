from streamlit.testing.v1 import AppTest

def test_app():
    at = AppTest.from_file("app.py")
    at.run()
    assert at.title[0].value is not None