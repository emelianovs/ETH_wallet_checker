import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(message)s")

console = logging.StreamHandler()
console.setLevel(logging.INFO)

logger = logging.getLogger(__name__)
