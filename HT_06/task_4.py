"""Написати функцію <prime_list>, яка прийматиме 2 аргументи - початок і кінець діапазона, і вертатиме список простих
чисел всередині цього діапазона. Не забудьте про перевірку на валідність введених даних та у випадку невідповідності
- виведіть повідомлення."""


def prime_list(start, finish):
    prime_nums = []
    for num in range(start, finish + 1):
        if num > 1:
            flag = True
            for i in range(2, int(num ** 0.5) + 1):
                if num % i == 0:
                    flag = False
                    break
            if flag:
                prime_nums.append(num)
    return prime_nums


try:
    first_num = input("enter first number: ")
    second_number = input("enter second number: ")
    print(prime_list(int(first_num),int(second_number)))
except ValueError:
    print("One of your values is not valid ,please try again input integer values")
