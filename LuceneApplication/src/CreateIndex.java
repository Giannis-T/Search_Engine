import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;

public class CreateIndex {
	
	protected String indexPath = "/SearchEngine/NewIndex";
	protected Directory directory;
	
	public CreateIndex() throws IOException {
	
		directory = FSDirectory.open(Paths.get(indexPath));
	}
	
	public void addFileToIndex() throws IOException {
		StandardAnalyzer analyzer = new StandardAnalyzer();
	    IndexWriterConfig indexWriterConfig = new IndexWriterConfig(analyzer);
	    Directory indexDirectory = FSDirectory.open(Paths.get(indexPath));
	    IndexWriter indexWriter = new IndexWriter(indexDirectory, indexWriterConfig);
	    String line = "";  
		String splitBy = "\t"; 
		String[] row;
		try   
		{  
			//parsing a CSV file into BufferedReader class constructor  
			BufferedReader br = new BufferedReader(new FileReader("C:\\Users\\Giannis\\Desktop\\SearchEngine\\data\\clean_songs.tsv"));  
			while ((line = br.readLine()) != null)   //returns a Boolean value  
			{  
				row = line.split(splitBy);    // use comma as separator
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
        // use a string field for isbn because we don't want it tokenized
//        doc.add(new StringField("isbn", isbn, Field.Store.YES));
        w.addDocument(doc);
    }
    
    public static void main(String[] args) throws IOException, ParseException {
    	CreateIndex index = new CreateIndex();
    	index.addFileToIndex();
    	System.out.println("Successful index creation. DONT RUN THIS AGAIN");
//    	
//    	// Testing if index is working
//		StandardAnalyzer analyzer = new StandardAnalyzer();
//    	String querystr = args.length > 0 ? args[0] : "beatles";
//		
//		// the "title" arg specifies the default field to use
//		// when no field is explicitly specified in the query.
//		Query q = new QueryParser("artist", analyzer).parse(querystr);
//		
//		// 3. search
//		int hitsPerPage = 20;
//		IndexReader reader = DirectoryReader.open(index.directory);
//		IndexSearcher searcher = new IndexSearcher(reader);
//		TopDocs docs = searcher.search(q, hitsPerPage);
//		ScoreDoc[] hits = docs.scoreDocs;
//		
//		// 4. display results
//		System.out.println("Found " + hits.length + " hits.");
//		for(int i=0;i<hits.length;++i) {
//		    int docId = hits[i].doc;
//		    Document d = searcher.doc(docId);
//		    System.out.println((i + 1) + ". " + d.get("artist") + "\t" + d.get("title")+ "\t" + d.get("lyrics"));
//		}
    	
    }
    
}
