/** An example of synchronization in Java.
 * @author: Kyle Benson
 * WInter 2013
 */

import java.util.Vector;

public class SynchronizationExample {
    static final int numThreads = 100;

    public static class Counter {
	private int count;
	public Counter(int start){
	    this.count = start;
	}

	public void increment(){
	    this.count = this.count + 1;
	}

	public void add(int toAdd) {
	    this.count += toAdd;
	}

	public int getCount(){
	    return count;
	}
    }

    /** This threaded class will simply increment a shared variable. */
    public static class CountingThread implements Runnable {
	private Counter sharedVar;

	public CountingThread (Counter theSharedVar) {
	    sharedVar = theSharedVar;
	}

	public void run() {
	    try {
		Thread.sleep(1000);
	    }
	    catch (InterruptedException e) {
		System.out.println("Interrupted!");
	    }

	    sharedVar.increment();
	}
    }

    public static void main(String args[]){
	Counter sharedVar = new Counter(0); //should be == numThreads when finished is synched properly.
	Vector<Thread> myThreads = new Vector<Thread>();

	for (int i = 0; i < numThreads; i++) {
	    myThreads.add(new Thread(new CountingThread(sharedVar)));
	}

	for (Thread t : myThreads) {
		t.start();
	}

	for (Thread t : myThreads) {
	    try {
		t.join();
	    }
	    catch (InterruptedException e) {
		System.out.println("Interrupted!");
	    }
	}

	System.out.format("Expecting sharedVar = %d\n", numThreads);
	System.out.format("Actual sharedVar = %d\n", sharedVar.getCount());
    }
}