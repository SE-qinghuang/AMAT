java.text.DateTimeFormatter timeParser = ISODateTimeFormat.timeParser();
TimeZone timeZone = TimeZone.getDefault();
System.out.println(timeZone.getID());
System.out.println(timeZone.getDisplayName());
DateTimeZone defaultTimeZone = DateTimeZone.getDefault();
System.out.println(defaultTimeZone.getID());
System.out.println(defaultTimeZone.getName(0L));
DateTime currentTime = new DateTime();
DateTimeZone currentZone = currentTime.getZone();
System.out.println(currentZone.getID());
System.out.println(currentZone.getName(0L));
