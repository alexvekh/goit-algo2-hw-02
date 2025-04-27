from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера
    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера
    Returns:
        Dict з порядком друку та загальним часом
    """

    # Вхідні словники в об'єкти PrintJob
    jobs = [PrintJob(**job) for job in print_jobs]
    # Обмеження в об'єкт PrinterConstraints
    printer = PrinterConstraints(**constraints)
    
    # Сортуємо за пріоритетом
    jobs.sort(key=lambda x: (x.priority))
    
    print_order = []
    total_time = 0

    # для підрахунку відповіності constraints
    current_batch = []  # поточна група на друк
    current_volume = 0 
    current_items = 0  

    for job in jobs:
        # Беремо завдання, перевіряємо чи можемо додати його до групи на друк, якщо можемо,- додаємо
        if (current_volume + job.volume <= printer.max_volume) and (current_items + 1 <= printer.max_items):
            current_batch.append(job)
            current_volume += job.volume
            current_items += 1
        else:
            # Якщо більшке не можемо додати,- завершуємо групу, записуємо до результатів. 
            if current_batch:
                total_time += max(j.print_time for j in current_batch)
                print_order.extend(j.id for j in current_batch)
            # Починаємо нову групу
            current_batch = [job]
            current_volume = job.volume
            current_items = 1

    # Після проходу всіх завдань записуємо залишок до результатів.
    if current_batch:
        total_time += max(j.print_time for j in current_batch)
        print_order.extend(j.id for j in current_batch)

    return {
        "print_order": print_order,
        "total_time": total_time
    }


# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},  # дипломна
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}  # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")

if __name__ == "__main__":
    test_printing_optimization()


# Очікуваний результат:

# Тест 1 (однаковий пріоритет):
# Порядок друку: ['M1', 'M2', 'M3']
# Загальний час: 270 хвилин

# Тест 2 (різні пріоритети):
# Порядок друку: ['M2', 'M1', 'M3']
# Загальний час: 270 хвилин

# Тест 3 (перевищення обмежень):
# Порядок друку: ['M1', 'M2', 'M3']
# Загальний час: 450 хвилин



 