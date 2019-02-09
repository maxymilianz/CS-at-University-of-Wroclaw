require 'drb'


log_server = DRbObject.new_with_uri('druby://localhost:9000')

log_server.log_message(21, 'Panie, oświetlaj mą drogę tak jak halogen')
log_server.log_message(37, 'Palę amnesia haze')
log_server.log_message(21, 'Świeć Panie nad duszą naszych wrogów')

time_0 = Time.now

log_server.log_message(37, 'W bani mam dziurę jak JFK')
log_server.log_message(21, 'A można, jak najbardziej. Jeszcze jak')
log_server.log_message(37, 'Wyprzedzam swoje czasy jakbym jeździł DeLoreanem')

time_1 = Time.now

log_server.log_message(21, 'Po co mam wybierać? Najlepiej wybrać obie')
log_server.log_message(37, 'Pozdrawiam załogę')

puts(log_server.report(time_0, time_1, 37, /./))
