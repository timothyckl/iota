import pytest

from iotadb.iotadb import Document, IotaDB


@pytest.fixture
def default_database():
    return IotaDB()


@pytest.fixture
def sample_documents():
    return [
        Document(
            id=0,
            text="The fluffy white cat danced gracefully across the sunlit room, casting delicate shadows on the walls.",
        ),
        Document(
            id=1,
            text="Lost in a labyrinth of thoughts, she sought refuge in the solace of her favorite book, its pages a sanctuary of escape.",
        ),
        Document(
            id=2,
            text="As the sun dipped below the horizon, painting the sky in hues of orange and pink, the world seemed to hold its breath in anticipation of the night's arrival.",
        ),
        Document(
            id=3,
            text="With a gentle breeze whispering through the trees, the scent of pine mingled with the fragrance of wildflowers, creating an intoxicating symphony of nature.",
        ),
        Document(
            id=4,
            text="Amidst the chaos of the bustling city streets, two strangers shared a fleeting glance, their eyes locking in a moment of unexpected connection before disappearing into the crowd.",
        ),
    ]
