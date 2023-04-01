import java.io.File;
import java.io.IOException;
import java.io.PrintStream;
import java.io.FileWriter;


class SearchModule {
    public static void main(String[] args) throws IOException {
        File file = new File("results.txt");
        FileWriter myWriter = new FileWriter(file);
        myWriter.write("Java Write: "+args[0]);
        // PrintStream stream = new PrintStream(new File("results.txt"))) {
        //     System.setOut(stream);
        // }
        // System.out.println("Java Write: "+args[0]);
        myWriter.close();
        System.out.println("Java Write: "+args[0]);

        
    }
}