class Test{ 
public static void main(String[] args){ 
DateTimeFormatter formatter = DateTimeFormat.forPattern( "MM/dd/yyyy" );
LocalDate past = formatter.parseLocalDate( "06/22/2010" );
DateTimeZone = DateTimeZone.forID( "America/Montreal" ): // match time zone intended for that input string.
int days = Days.daysBetween( past, LocalDate.now( timeZone ) );
}
}