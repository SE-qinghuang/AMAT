import   java.text.DateTimeFormatter
import   java.util.DateTime
import   java.util.TimeZone
import   java.util.DateTimeZone
public class Test{ 
public static void main(String[] args){ 
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
}
}

File mFile = new File("src/lt/test.txt");
FileInputStream fis = new FileInputStream(mFile);
BufferedReader br = new BufferedReader(fis);
String result = "";
String line = "";
while( (line = br.readLine()) != null){
		result = result + line;
		}
public class Test{ 
public static void main(String[] args){ 
File mFile = new File(src/lt/test.txt); 
 	FileInputStream fis = new FileInputStream(mFile); 
 	BufferedReader br = new BufferedReader(fis); 
 	String result = "; 
 	String line = "; 
 	while( (line = br.readLine()) != null){		result = result + line; 
 	}
}
}import   java.util.DateTime
import   java.util.DateTimeZone
import   java.text.DateTimeFormatter
import   java.util.TimeZone
public class Test{ 
public static void main(String[] args){ 
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
 
}
}