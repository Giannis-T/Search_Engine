import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Paths;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.store.NIOFSDirectory;

public class CreateIndex {
	
	protected String indexPath = "/SearchEngine/LuceneIndex";
	protected Directory directory;
	
	public CreateIndex() throws IOException {
		
		directory = new NIOFSDirectory(Paths.get(indexPath));
	}
	
	public void addFileToIndex() throws IOException {
		StandardAnalyzer analyzer = new StandardAnalyzer();
	    IndexWriterConfig indexWriterConfig = new IndexWriterConfig(analyzer);
	    Directory indexDirectory = FSDirectory.open(Paths.get(indexPath));
	    IndexWriter indexWriter = new IndexWriter(indexDirectory, indexWriterConfig);
    	indexWriter.deleteAll();
	    String line = "";  
		String splitBy = "\t"; 
		String[] row;
		try   
		{  
			BufferedReader br = new BufferedReader(new FileReader("C:\\Users\\Giannis\\Desktop\\SearchEngine\\data\\clean_songs.tsv"));  
			while ((line = br.readLine()) != null)     
			{  
				row = line.split(splitBy);    
			    	addDoc(indexWriter, row[0], row[1], row[2]);
				}  
				indexWriter.close();
		}   
		catch (IOException e)   
		{  
			e.printStackTrace();  
		}
		
		
	}
    private void addDoc(IndexWriter w, String artist, String title, String lyrics) throws IOException {
        Document doc = new Document();
        doc.add(new TextField("artist", artist, Field.Store.YES));
        doc.add(new TextField("title", title, Field.Store.YES));
        doc.add(new TextField("lyrics", lyrics, Field.Store.YES));
        w.addDocument(doc);
    }
    
    public static void main(String[] args) throws IOException, ParseException {
    	CreateIndex index = new CreateIndex();
    	index.addFileToIndex();
    	System.out.println("Successful index creation. DONT RUN THIS AGAIN");
    	
    }
    
}
