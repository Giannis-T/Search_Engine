 import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Paths;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
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
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.search.highlight.Fragmenter;
import org.apache.lucene.search.highlight.Highlighter;
import org.apache.lucene.search.highlight.InvalidTokenOffsetsException;
import org.apache.lucene.search.highlight.QueryScorer;
import org.apache.lucene.search.highlight.SimpleHTMLFormatter;
import org.apache.lucene.search.highlight.SimpleSpanFragmenter;
import org.apache.lucene.search.highlight.TextFragment;
import org.apache.lucene.search.highlight.TokenSources;

import com.opencsv.CSVReader;

import org.apache.lucene.store.ByteBuffersDirectory;

import java.util.Formatter;
import java.util.Scanner;


public class SearchModule {
	
	
	public static void main(String[] args) throws IOException, ParseException, InvalidTokenOffsetsException {
		StandardAnalyzer analyzer = new StandardAnalyzer();
		
    	String querystr = args[0];
		String field = args[1];
		int pageNumber = Integer.parseInt(args[2]);
		int hitsPerPage = 10;
		
		Query q = new QueryParser(field, analyzer).parse(querystr);
		
		// 3. search
		
		IndexReader reader = DirectoryReader.open(FSDirectory.open(Paths.get("/SearchEngine/src/index")));
		IndexSearcher searcher = new IndexSearcher(reader);
	    TopScoreDocCollector collector = TopScoreDocCollector.create(hitsPerPage * pageNumber, Integer.MAX_VALUE);
	  
	    
	    SimpleHTMLFormatter htmlFormatter = new SimpleHTMLFormatter();	    
	    QueryScorer queryScorer = new QueryScorer(q);
	    Highlighter highlighter = new Highlighter(htmlFormatter, queryScorer);
	    highlighter.setTextFragmenter(new SimpleSpanFragmenter(queryScorer, Integer.MAX_VALUE));
	    highlighter.setMaxDocCharsToAnalyze(Integer.MAX_VALUE);
//	    
        searcher.search(q, collector);
        
	    ScoreDoc[] hits = collector.topDocs((pageNumber - 1) * hitsPerPage, hitsPerPage).scoreDocs;

		// 4. display results
		System.out.println("Found " + hits.length + " hits.");
		for(int i=0;i<hits.length;++i) {
		    int docId = hits[i].doc;
		    Document d = searcher.doc(docId);
		    if (field.equals("artist")) {
			    System.out.println("###"+(i + 1) + "$$$" + (highlighter.getBestFragment(analyzer, field, d.get(field))) + "$$$" + d.get("title")+ "$$$" + d.get("lyrics"));
		    }
		    else if (field.equals("title")){
			    System.out.println("###"+(i + 1) + "$$$" + d.get("artist") + "$$$" + (highlighter.getBestFragment(analyzer, field, d.get(field)))+ "$$$" + d.get("lyrics"));

		    }
		    else {
			    System.out.println("###"+(i + 1) + "$$$" + d.get("artist") + "$$$" + d.get("title")+ "$$$" + (highlighter.getBestFragment(analyzer, field, d.get(field))));

		    }
//		    System.out.println("###"+(i + 1) + "$$$" + d.get("artist") + "$$$" + d.get("title")+ "$$$" + d.get("lyrics"));
             
		}
			
		reader.close();
	}		
}