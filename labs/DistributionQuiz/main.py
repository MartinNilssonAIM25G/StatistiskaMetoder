from labs.distribution_quiz import DistributionQuiz
import matplotlib.pyplot as plt

if __name__ == "__main__":
    quiz = DistributionQuiz()
    print("Welcome to Distribution Quiz!")
    print("Time to guess which distribution is shown in the graph\n")
    
    while True:
        correct_key = quiz.rng.choice(list(quiz.distribution.keys()))
        correct_name, generate_function = quiz.distribution[correct_key]  # <-- Använd correct_key här!
        data = generate_function()
        
        print("\nWhich distribution are we looking at?")
        for key, (name, _) in quiz.distribution.items():
            print(f"{key}. {name}")
        print("\nThe graph will open... study it and close the window to answer.\n")
        
        quiz.show_distribution(data, show_type='histogram')    
        
        answer = input("Your answer (or 'q' to quit): ")
        
        if answer.lower() == 'q':
           print(f"\nFinal score: {quiz.score}")
           break
           
        if answer == correct_key:
            print("✓ Correct!")
            quiz.score += 1
        else:
            print(f"✗ Incorrect! It was {correct_name}")
            
        print(f"Score: {quiz.score}\n")
        plt.close()