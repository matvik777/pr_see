class TestClass:
    def __del__(self):
        print("Объект удалён")

test = TestClass()
del test  # Выведет: "Объект удалён"
