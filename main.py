import streamlit as st


def mod(number, modulus):
    return number % modulus

def primeFactorisation(number):
    prime_dict = {}
    for i in range(2,number+1):
        if number % i == 0:
            prime_dict[i] = 0
            while number % i == 0:
                prime_dict[i] += 1
                number /= i
    return prime_dict

def modularInverse(number, modulus):
    for i in range(modulus):
        
        if mod(number * i, modulus) == 1:
            return i

    

def gcd(a,b):
    
    while b != 0:
        (a, b) = (b, a % b)
    return a

def primePowers(number):
    number = primeFactorisation(number)
    prime_powers = []
    for key in number:
        prime_powers.append(key ** number[key])

    return prime_powers

def Reducing_mods(new_mods):
    for i in range(len(new_mods)):
            for j in range(len(new_mods)):
                if i != j and j < i:
                    first_mod_factorisation = primeFactorisation(new_mods[i][1])
                    second_mod_factorisation = primeFactorisation(new_mods[j][1])
                    for prime in first_mod_factorisation:
                        if prime in second_mod_factorisation:
                            if first_mod_factorisation[prime] > second_mod_factorisation[prime]:
                                if mod(new_mods[i][0],new_mods[j][1]) == mod(new_mods[j][0],new_mods[j][1]):
                                    new_mods.pop(j)
                                    return Reducing_mods(new_mods)
                                else:
                                    return f"Contradiction: {new_mods[i][0]} mod {new_mods[j][1]} does not equal {new_mods[j][0]}"
                            if first_mod_factorisation[prime] < second_mod_factorisation[prime]:
                                
                                if mod(new_mods[j][0],new_mods[i][1]) == mod(new_mods[i][0],new_mods[i][1]):
                                    new_mods.pop(i)
                                    return Reducing_mods(new_mods)
                                else:
                                    
                                    return f"Contradiction: {new_mods[j][0]} mod {new_mods[i][1]} does not equal {new_mods[i][0]} mod {new_mods[i][1]}"

                            if first_mod_factorisation[prime] == second_mod_factorisation[prime]:
                                if new_mods[i][0] == new_mods[j][0]:
                                    new_mods.pop(i)
                                    return Reducing_mods(new_mods)
                                else:
                                    return f"Contradiction: {new_mods[i][0]} mod {new_mods[i][1]} does not equal {new_mods[j][0]} mod {new_mods[j][1]}"

    return new_mods

def are_all_coprime(mods):
    for i in range(len(mods)):
        for j in range(i):
            if gcd(mods[i], mods[j]) != 1:
                return False
    return True

def ChineseRemainderTheorem(list):
    ''' expects a list of tuples of form [(number,mod), (number, mod), ...]'''
    
    solution = 0
    mods = [entry[1] for entry in list]
    
    numbers = [entry[0] for entry in list]
    
    if are_all_coprime(mods) == True:
        N = 1
        for entry in mods:
            N *= entry
        
        for i in range(len(mods)):
            Ni = N / mods[i]
            xi = modularInverse(Ni,mods[i])
            solution += (Ni * xi * int(numbers[i]))
    else:
        new_mods = []
        for entry in list:
            
            mod_prime_powers = primePowers(entry[1])
            for power in mod_prime_powers:
                
                new_mods.append((mod(entry[0],power),power))

        
        new_list = Reducing_mods(new_mods)
        return ChineseRemainderTheorem(new_list)
        
                    
                                
                            
                            
                                
                    
            
        
   
    return (mod(solution,N),N)
            
        
st.title("Chinese Remainder Theorem Calculator")

st.text("This is a calculator that can solve simultaneous congruences using chinese remainder theorem")


if "num_congruences" not in st.session_state:
    st.session_state.num_congruences = 1


if st.button("➕ Add Congruence"):
    st.session_state.num_congruences += 1

congruences = []


for i in range(st.session_state.num_congruences):
    col1, col2, col3 = st.columns([2,1,2])

    with col1:
        a = st.text_input(
            f"a{i}", 
            placeholder="Enter value a", 
            label_visibility="collapsed"
        )
    with col2:
        st.markdown(
            "<div style='text-align:center; font-size:20px; margin-top:6px;'>mod</div>",
            unsafe_allow_html=True,
        )
    with col3:
        n = st.text_input(
            f"n{i}", 
            placeholder="Enter modulus n", 
            label_visibility="collapsed"
        )

    congruences.append((a, n))

if st.button("Run Calculator"):
    int_congruences = [(int(a), int(n)) for a, n in congruences if a and n]
    result = ChineseRemainderTheorem(int_congruences)
    if type(result) == str:
        st.error(result)

    else:
        st.markdown(f"x = {int(result[0])} mod {result[1]}")


