import streamlit as st
import pickle
from datetime import datetime
startTime = datetime.now()

filename = "modelForest.sv"
model = pickle.load(open(filename,'rb'))

class_number_d = {1:"pierwsza",2:"druga",3:"trzecia",4:"czwarta"}
learning_time_d = {0:"wcale",1:"kilka minut",2:"około godziny",3:"2 do 5 godzin",4:"powyżej 5 godzin"}
learning_intensity_d = {0:"wcale",1:"pobieżnie",2:"wystarczająco",3:"skrupulatnie",4:"kompleksowo"}
actualMotivation_d = {1:"bardzo niska",2:"niska",3:"przeciętna",4:"wysoka",5:"bardzo wysoka"}
gradePredictions_d = {1:"bardzo niskie",2:"niskie",3:"średnie",4:"wysokie",5:"bardzo wysokie"}
teacher_d = {1:"nie będzie zwracał uwagi",2:"będzie skrupulatnie pilnował",3:"będzie dbał o prawidłowy przebieg"}
sex_d = {1:"mężczyzna", 2:"kobieta", 3:"nie chcę podawać"}
subject_d = {1:"maturalny", 2:"zawodowy", 3:"inny"}
questions_d = {1:"nie zaskoczą mnie", 2:"mogą mnie zaskoczyć"}

def main():

    st.set_page_config(page_title="Aplikacja przewidująca ocenę ze sprawdzianu/pracy klasowej")
    overview = st.container()
    upper_left, upper_right = st.columns(2)
    left, middle1, middle2, right = st.columns(4)
    prediction = st.container()

    with overview:
        st.title("Typowanie oceny z pracy pisemnej")

    with upper_left:
        zrodla = ['podręcznik', 
                  'notatki', 
                  'dodatkowe notatki', 
                  'aplikacje', 
                  'strony www', 
                  'fiszki', 
                  'dodatkowe książki']
        selected_zrodla = st.multiselect('Wybierz źródła wiedzy', zrodla)

        from_coursebook = 1 if 'podręcznik' in selected_zrodla else 0
        from_notebook = 1 if 'notatki' in selected_zrodla else 0
        from_many_notebooks = 1 if 'dodatkowe notatki' in selected_zrodla else 0
        from_apps = 1 if 'aplikacje' in selected_zrodla else 0
        from_websites = 1 if 'strony www' in selected_zrodla else 0
        from_flashards = 1 if 'fiszki' in selected_zrodla else 0
        from_books = 1 if 'dodatkowe książki' in selected_zrodla else 0

        options_motivate = ['dobra ocena', 
                            'zainteresowanie przedmiotem', 
                            'pozytywna ocena', 
                            'zadowolenie rodziców/opiekunów', 
                            'przyszła praca', 
                            'przyszłe studia',
                            'brak czynników']
        selected_options_motivate = st.multiselect('Wybierz czynniki motywujące', options_motivate)
        
        prosGoodMark = 1 if 'dobra ocena' in selected_options_motivate else 0
        prosInterest = 1 if 'zainteresowanie przedmiotem' in selected_options_motivate else 0
        prosPositivMark = 1 if 'pozytywna ocena' in selected_options_motivate else 0
        prosJoy = 1 if 'zadowolenie rodziców/opiekunów' in selected_options_motivate else 0
        prosJob = 1 if 'przyszła praca' in selected_options_motivate else 0
        prosStudies = 1 if 'przyszłe studia' in selected_options_motivate else 0
        
        if 'brak czynników' in selected_options_motivate:
            prosGoodMark = 0
            prosInterest = 0
            prosPositivMark = 0
            prosJoy = 0
            prosJob = 0
            prosStudies = 0
            prosNone = 1
        else:
            prosNone = 0

    with upper_right:
        options_przeciw = ['złe samopoczucie', 
                           'napięty plan zajęć', 
                           'niechęć do przedmiotu', 
                           'czas spędzony na rozrywce', 
                           'bogate życie towarzyskie', 
                           'nie ma żadnych']
        selected_options_przeciw = st.multiselect('Wybierz czynniki przeciw', options_przeciw)
        
        badWellBeing = 1 if 'złe samopoczucie' in selected_options_przeciw else 0
        busySchedule = 1 if 'napięty plan zajęć' in selected_options_przeciw else 0
        hatred_to_subject = 1 if 'niechęć do przedmiotu' in selected_options_przeciw else 0
        entertainment = 1 if 'czas spędzony na rozrywce' in selected_options_przeciw else 0
        richSocialLife = 1 if 'bogate życie towarzyskie' in selected_options_przeciw else 0
        if 'nie ma żadnych' in selected_options_przeciw:
            badWellBeing = 0
            busySchedule = 0
            hatred_to_subject = 0
            entertainment = 0
            richSocialLife = 0
            badFactorsNone = 1
        else:
            badFactorsNone = 0

        options_za = ['pozytywna postawa', 
                      'determinacja', 
                      'umiejętność zarządzania czasem', 
                      'umiejętność ułożenia planu nauki', 
                      'rezygnacja z rozrywki', 
                      'BRAK']
        selected_options_za = st.multiselect('Wybierz czynniki za', options_za)

        goodAttitude = 1 if 'pozytywna postawa' in selected_options_za else 0
        determination = 1 if 'determinacja' in selected_options_za else 0
        goodSchedule = 1 if 'umiejętność zarządzania czasem' in selected_options_za else 0
        goodScheduleLearn = 1 if 'umiejętność ułożenia planu nauki' in selected_options_za else 0
        joyResignation = 1 if 'rezygnacja z rozrywki' in selected_options_za else 0
        if 'BRAK' in selected_options_za:
            goodAttitude = 0
            determination = 0
            goodSchedule = 0
            goodScheduleLearn = 0
            joyResignation = 0
            goodFactorsNone = 1
        else:
            goodFactorsNone = 0

    with left:
        sex = st.radio("Płeć", list(sex_d.keys()), format_func= lambda x: sex_d[x])
        if sex == 1:
            sex_man = 1
            sex_woman = 0
            sex_notGiven = 0
        elif sex == 2:
            sex_man = 0
            sex_woman = 1
            sex_notGiven = 0
        elif sex == 3:
            sex_man = 0
            sex_woman = 0
            sex_notGiven = 1
        
        class_number = st.radio("Klasa", list(class_number_d.keys()), format_func= lambda x: class_number_d[x])
        subject = st.radio("Przedmiot", list(subject_d.keys()), format_func= lambda x: subject_d[x])
        if subject == 1:
            subject_grad = 1
            subject_prof = 0
            subject_other = 0
        elif subject == 2:
            subject_grad = 0
            subject_prof = 1
            subject_other = 0
        elif subject == 3:
            subject_grad = 0
            subject_prof = 0
            subject_other = 1

    with middle1:
        learning_time = st.radio("Czas nauki", list(learning_time_d.keys()), format_func= lambda x: learning_time_d[x])
        learning_intensity = st.radio("Intensywność nauki", list(learning_intensity_d.keys()), format_func= lambda x: learning_intensity_d[x])

    with middle2:
        teacher = st.radio("Nauczyciel podczas sprawdzianu", list(teacher_d.keys()), format_func= lambda x: teacher_d[x])
        if teacher == 1:
            teacher_behaviour_inert = 1
            teacher_behaviour_watch = 0
            teacher_behaviour_normal = 0
        elif teacher == 2:
            teacher_behaviour_inert = 0
            teacher_behaviour_watch = 1
            teacher_behaviour_normal = 0
        elif teacher == 3:
            teacher_behaviour_inert = 0
            teacher_behaviour_watch = 0
            teacher_behaviour_normal = 1

        questions = st.radio("Pytania", list(questions_d.keys()), format_func= lambda x: questions_d[x])
        if questions == 1:
            questions_notSurprised = 1
            questions_surprised = 0
        elif questions == 2:
            questions_notSurprised = 0
            questions_surprised = 1
        
    with right:
        actual_motivation = st.radio("Motywacja aktualnie", list(actualMotivation_d.keys()), format_func= lambda x: actualMotivation_d[x])
        gradePredictions = st.radio("Twoje przewidywanie", list(gradePredictions_d.keys()), format_func= lambda x: gradePredictions_d[x])

    data = [[class_number, learning_time, learning_intensity, from_coursebook, from_notebook, from_many_notebooks, from_apps, from_websites, from_flashards, from_books, prosGoodMark, prosInterest, prosPositivMark, prosJoy, prosJob, prosStudies, prosNone, badWellBeing, busySchedule, hatred_to_subject, entertainment, richSocialLife, badFactorsNone, goodAttitude, determination, goodSchedule, goodScheduleLearn, joyResignation, goodFactorsNone, actual_motivation, gradePredictions, subject_other, subject_grad, subject_prof, teacher_behaviour_inert, teacher_behaviour_normal, teacher_behaviour_watch, questions_notSurprised, questions_surprised, sex_man, sex_notGiven, sex_woman]]  
    oceny = model.predict(data)
    s_confidence = model.predict_proba(data)
    if learning_time > 2 and learning_intensity > 2 and oceny[0] < 4:
        oceny[0] += 1
    if learning_time < 2 and learning_intensity < 2 and gradePredictions > 4:
        gradePredictions = 2
        oceny[0] = 2
    tekst = "Wskazane parametry przewidują ocenę: "
    if oceny[0] == 1:
        tekst += "Niedostateczna"
    elif oceny[0] == 2:
        tekst += "Dopuszczająca"
    elif oceny[0] == 3:
        tekst += "Dostateczna"
    elif oceny[0] == 4:
        tekst += "Dobra"
    elif oceny[0] == 5:
        tekst += "Bardzo dobra"
    elif oceny[0] == 6:
        tekst += "Celująca"
    with prediction:
        st.subheader(tekst)
        st.write("Pewność predykcji {0:.2f} %".format(s_confidence[0][oceny][0] * 100))
        st.write("Przewidywania oparte na podstawie odpowiedzi ankietowych uczniów szkoły ponadpodstawowej")

if __name__ == "__main__":
    main()