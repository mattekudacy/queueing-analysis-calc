import streamlit as st

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

def calculate_single_server_parameters(arrival_rate, service_rate):
    po = round(1 - (arrival_rate / service_rate), 2)
    l = arrival_rate / (service_rate - arrival_rate)
    lq = (arrival_rate ** 2) / (service_rate * (service_rate - arrival_rate))
    w = round(1 / (service_rate - arrival_rate), 3)
    wq = round(arrival_rate / (service_rate * (service_rate - arrival_rate)), 3)
    p = arrival_rate / service_rate
    i = round(1 - p, 3)

    return po, l, lq, w, wq, p, i

def calculate_multiple_server_parameters(arrival_rate, service_rate, s, n):
    s_service_rate = s * service_rate

    p_fact = 1 + sum([(1 / factorial(i)) * ((arrival_rate / service_rate) ** i) for i in range(1, s)])
    p_fact2 = (1 / factorial(s)) * ((arrival_rate / service_rate) ** s)
    p_fact3 = s_service_rate / (s_service_rate - arrival_rate)
    p0 = round(1 / (p_fact + (p_fact2 * p_fact3)), 3)

    num = (arrival_rate * service_rate * ((arrival_rate / service_rate) ** s))
    denam = factorial(s-1) * (((s * service_rate) - arrival_rate) ** 2)
    l = round((num / denam)  * p0 + arrival_rate / service_rate, 1)
 
    w = l / arrival_rate

    lq = round(l - (arrival_rate / service_rate), 2)

    wq = round(lq / arrival_rate, 2)

    pw = round((1 / factorial(s) * ((arrival_rate / service_rate) ** s)) * (s*service_rate / (s*service_rate - arrival_rate)) * p0, 3)

    if n > s:
        pn = round((1 / (factorial(s) * s ** (n - s))) * ((arrival_rate / service_rate) ** n) * p0, 1)
    elif n <= s:
        pn = round((1 / factorial(n)) * ((arrival_rate / service_rate) ** n) * p0, 1)

    return p0, l, w, lq, wq, pw, pn

def main():
    st.title("Analysis of Queueing System Calculator")

    options = st.sidebar.radio("Select Queueing Model", ("Basic Single Server Model", "Basic Multiple Server Model"))

    if options == "Basic Single Server Model":
        arrival_rate = st.text_input("λ - Arrival Rate", "24")
        service_rate = st.text_input("μ - Service Rate", "30")

        arrival_rate = int(arrival_rate)
        service_rate = int(service_rate)

        if st.button("Calculate"):
            po, l, lq, w, wq, p, i = calculate_single_server_parameters(arrival_rate, service_rate)

            st.write(f"Probability that no customers are in the queueing system")
            st.latex(r'P_0 = (1 - \frac{{\lambda}}{{\mu}}) = (1 - \frac{{{}}}{{{}}}) = {}'.format(arrival_rate, service_rate, po))
            st.markdown(f'<div style="text-align: center"><b>{po}</b> probability of no customers in system</div>', unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write(f"Average number of customer in queueing system")
            st.latex(r'L = \frac{{\lambda}}{{\mu - \lambda}} = \frac{{{}}}{{{} - {}}} = {}'.format(arrival_rate, service_rate, arrival_rate, int(l)))
            st.markdown(f'<div style="text-align: center"><b>{int(l)}</b> customer/s on the average in the queueing system</div>', unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write(f"Average number of customers in waiting line")
            st.latex(r'L_q = \frac{{\lambda^2}}{{\mu(\mu - \lambda)}} = \frac{{{}^2}}{{{}({} - {})}} = {}'.format(arrival_rate, service_rate, service_rate, arrival_rate, lq))
            st.markdown(f'<div style="text-align: center"><b>{lq}</b> customer/s on the average in the waiting line</div>', unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write(f"Average time customer spends in the queueing system")
            st.latex(r'W = \frac{{1}}{{\mu - \lambda}} = \frac{{1}}{{{} - {}}} = {}'.format(service_rate, arrival_rate, w))
            st.markdown(f'<div style="text-align: center"><b>{w}</b> hour/s {round(w* 60)} minutes average time in system per server</div>', unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write(f"Average time customer spends waiting in line")
            st.latex(r'W_q = \frac{{\lambda}}{{\mu(\mu - \lambda)}} = \frac{{{}}}{{{}({} - {})}} = {}'.format(arrival_rate, service_rate, service_rate, arrival_rate, wq))
            st.markdown(f'<div style="text-align: center"><b>{wq}</b> hour/s {round(wq* 60)} minutes average time in system per customer</div>', unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write(f"Probability that server is busy and a customer has to wait**{p}**")
            st.latex(r'p = \frac{{\lambda}}{{\mu}} = \frac{{{}}}{{{}}} = {}'.format(arrival_rate, service_rate, p))
            st.markdown(f'<div style="text-align: center"><b>{p}</b> probability that the server will be busy and the customer must wait</div>', unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write(f"Probability that server is idle and customer can be served")
            st.latex(r'i = 1 - p = 1 - {} = {}'.format(p, i))
            st.markdown(f'<div style="text-align: center"><b>{i}</b> probability that the server will be idle and a customer can be served</div>', unsafe_allow_html=True)

    elif options == "Basic Multiple Server Model":
        arrival_rate = st.text_input("Arrival Rate", "10")
        service_rate = st.text_input("Service Rate", "4")
        s = st.text_input("Number of Servers (s)", "3")
        n = st.text_input("Number of Customers (n)", "3")

        arrival_rate = int(arrival_rate)
        service_rate = int(service_rate)
        s = int(s)
        n = int(n)

        if st.button("Calculate"):
            p0, l, w, lq, wq, pw, pn = calculate_multiple_server_parameters(arrival_rate, service_rate, s, n)

            st.write(f"Probability that there are no customers in systen")
            st.latex(r'P_0 = \frac{1}{{\left[\sum_{{i=1}}^{{n \atop s-1}} \frac{1}{{i!}} \left(\frac{\lambda}{\mu}\right)^i \right] + \frac{1}{{s!}} \left(\frac{\lambda}{\mu}\right)^s \left(\frac{s\mu}{s\mu - \lambda}\right)}} = ' + str(p0))
            st.markdown(f'<div style="text-align: center"><b>{p0}</b> probability that no customers are in the service.</div>', unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write(f"Average number of customer in queueing system")
            st.latex(r'L = \frac{{\lambda\mu(\lambda/\mu)^2}}{{(s-1)! [s\mu - \lambda]^2}}P_0 + \frac{{\lambda}}{{\mu}} = \frac{{({})({})({}/{})^2}}{{({}-1)! [{}({}) - {}]^2}}{} + \frac{{{}}}{{{}}} = {}'.format(arrival_rate, service_rate, arrival_rate, service_rate, s, s, service_rate, arrival_rate, p0, arrival_rate, service_rate, l, arrival_rate, l))
            st.markdown(f'<div style="text-align: center"><b>{int(l)}</b> customer/s in the service</div>', unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write(f"Average time customer spends in the queueing system")
            st.latex(r'W = \frac{{L}}{{\lambda}} = \frac{{{}}}{{{}}} = {}'.format(int(l), arrival_rate, w))
            st.markdown(f'<div style="text-align: center"><b>{w}</b> hour/s {round(w* 60)} minutes average time in the service</div>', unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write(f"Average number of customers in waiting line")
            st.latex(r'L_q = L - \frac{{\lambda}}{{\mu}} = {} - \frac{{{}}}{{{}}} = {}'.format(int(l), arrival_rate, service_rate, lq))
            st.markdown(f'<div style="text-align: center"><b>{lq}</b> customer/s waiting to be served</div>', unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write(f"Average time customer spends waiting in line")
            st.latex(r'W_q = \frac{{L_q}}{{\lambda}} = \frac{{{}}}{{{}}} = {}'.format(lq, arrival_rate, wq))
            st.markdown(f'<div style="text-align: center"><b>{wq}</b> hour/s {round(wq* 60)} minutes waiting in line</div>', unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write(f"Probability that the customer must wait")
            st.latex(r'P_w = \frac{{1}}{{s!}} (\frac{{\lambda}}{{\mu}})^s \frac{{s\mu}}{{s\mu - \lambda}}P_0 = \frac{{1}}{{{}!}} (\frac{{{}}}{{{}}})^{} \frac{{{}({})}} {{{}({}) - {}}}{} = {}'.format(s, arrival_rate, service_rate, s, s, service_rate, s, service_rate, arrival_rate, p0, pw))
            st.markdown(f'<div style="text-align: center"><b>{pw}</b> probability that a customer must wait for service</div>', unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write(f"Probability of n customers in the system")
            if n > s:
                st.latex(r'P_n = \frac{{1}}{{s!s^n-s}}(\frac {{\lambda}}{{\mu}})^nP_0 = \frac{{1}}{{{}!{}^{}-{}}}(\frac{{{}}}{{{}}})^{}{} = {}'.format(s, s, n, s, arrival_rate, service_rate, n, p0, pn))
                st.markdown(f'<div style="text-align: center"><b>{pn}</b> probability that there are <b>{n}</b> customers in the system</div>', unsafe_allow_html=True)
            else:
                st.latex(r'P_n = \frac{{1}}{{n!}}(\frac {{\lambda}}{{\mu}})^nP_0 = \frac{{1}}{{{}!}}(\frac{{{}}}{{{}}})^{}{} = {}'.format(n, arrival_rate, service_rate, n, p0, pn))
                st.markdown(f'<div style="text-align: center"><b>{pn}</b> probability that there are <b>{n}</b> customers in the system</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
